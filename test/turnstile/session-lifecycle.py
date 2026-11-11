#!/usr/bin/env python3
"""Exercise a staged Turnstile package without changing the host login stack.

Run as root on Linux with mount/PID namespaces enabled:
  python3 test/turnstile/session-lifecycle.py /path/to/pkg/turnstile

Requires Python, installed runtime libraries/PAM modules, and a staged package
from `mere dev build`. No package import or system installation is performed.
"""
import argparse
import ctypes
import glob
import json
import os
from pathlib import Path
import select
import shutil
import signal
import socket
import stat
import subprocess
import sys
import tempfile
import time
import traceback


# Python 3.14 lazily imports its ctypes layout code; load it before chroot.
class _PreloadCtypesLayout(ctypes.Structure):
    _fields_ = [("unused", ctypes.c_int)]


def wait_for(predicate, description, timeout=8):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if predicate():
            return
        time.sleep(0.05)
    raise AssertionError("timed out: " + description)


def populate(root, package):
    # tempfile's mode 0700 would prevent unprivileged helpers traversing '/'.
    root.chmod(0o755)
    for directory in ("bin", "lib/security", "usr/lib", "usr/bin", "etc/pam.d",
                      "etc/security", "run", "proc", "dev", "tmp",
                      "home/alice", "home/greeter", "root", "var/log"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    # Dereference store links: the chroot must not need the host Mere store.
    for directory in ("lib", "usr/lib", "lib/security"):
        for source in glob.glob("/" + directory + "/*.so*"):
            if os.path.isfile(source):
                shutil.copy2(source, root / directory / Path(source).name)
    shutil.copy2(package / "usr/bin/turnstiled", root / "usr/bin/turnstiled")
    shutil.copy2(package / "lib/security/pam_turnstile.so",
                 root / "lib/security/pam_turnstile.so")
    shutil.copytree(package / "etc-defaults", root / "etc", dirs_exist_ok=True)
    for name in ("dinit", "dinitctl", "dinit-monitor", "env", "sh", "cat", "mkdir", "sleep", "kill"):
        shutil.copy2("/bin/" + name, root / "bin" / name)
    shutil.copytree(package / "usr/libexec", root / "usr/libexec", dirs_exist_ok=True)
    fixtures = root / "etc/dinit-test"
    fixtures.mkdir()
    shutil.copy2(package / "usr/share/dinit.d/turnstiled", fixtures / "turnstiled")
    # Isolated fixture, not a substitute for testing the real boot graph.
    (fixtures / "sysinit").write_text("type = internal\n")
    (fixtures / "probe").write_text(
        "type = scripted\ncommand = /bin/sh /usr/bin/probe-ready\n"
        "depends-on = turnstiled\n")
    (root / "usr/bin/probe-ready").write_text(
        "[ -S /run/turnstiled/control.sock ] || exit 1\n"
        ": > /run/probe-ready\n")
    (root / "etc/passwd").write_text(
        "root:x:0:0:root:/root:/bin/sh\n"
        "alice:x:1000:1000:Alice:/home/alice:/bin/sh\n"
        "greeter:x:1001:1001:Greeter:/home/greeter:/bin/sh\n")
    (root / "etc/group").write_text(
        "root:x:0:\nalice:x:1000:\ngreeter:x:1001:\n")
    (root / "etc/security/limits.conf").write_text("")
    (root / "etc/pam.d/runtime-test").write_text(
        "session required pam_turnstile.so\n")
    for name, uid in (("alice", 1000), ("greeter", 1001)):
        os.chown(root / "home" / name, uid, uid)
    services = root / "usr/lib/dinit.d/user"
    (services / "boot.d").mkdir(parents=True)
    (services / "user-probe").write_text(
        "type = process\ncommand = /bin/sh /usr/bin/user-probe\nrestart = true\n")
    (services / "boot.d/user-probe").symlink_to("../user-probe")
    (root / "usr/bin/user-probe").write_text(
        "printf '%s\\n' \"$$\" > \"$XDG_RUNTIME_DIR/probe.pid\"\n"
        "exec /bin/sleep 300\n")
    os.chmod(root / "tmp", 0o1777)
    os.mknod(root / "dev/null", stat.S_IFCHR | 0o666, os.makedev(1, 3))
    os.chmod(root / "dev/null", 0o666)


def pam_worker(channel, username):
    class Message(ctypes.Structure):
        _fields_ = [("style", ctypes.c_int), ("message", ctypes.c_char_p)]

    class Response(ctypes.Structure):
        _fields_ = [("response", ctypes.c_char_p), ("code", ctypes.c_int)]

    callback_type = ctypes.CFUNCTYPE(
        ctypes.c_int, ctypes.c_int,
        ctypes.POINTER(ctypes.POINTER(Message)),
        ctypes.POINTER(ctypes.POINTER(Response)), ctypes.c_void_p)

    @callback_type
    def no_conversation(count, messages, responses, data):
        return 19  # PAM_CONV_ERR; these session-only tests must not prompt.

    class Conversation(ctypes.Structure):
        _fields_ = [("callback", callback_type), ("data", ctypes.c_void_p)]

    pam = ctypes.CDLL("/lib/libpam.so.0")
    pam.pam_start.argtypes = [ctypes.c_char_p, ctypes.c_char_p,
                              ctypes.POINTER(Conversation),
                              ctypes.POINTER(ctypes.c_void_p)]
    for name in ("pam_open_session", "pam_close_session", "pam_end"):
        getattr(pam, name).argtypes = [ctypes.c_void_p, ctypes.c_int]
    pam.pam_getenv.argtypes = [ctypes.c_void_p, ctypes.c_char_p]
    pam.pam_getenv.restype = ctypes.c_char_p
    handle = ctypes.c_void_p()
    conversation = Conversation(no_conversation, None)
    result = pam.pam_start(b"runtime-test", username.encode(),
                           ctypes.byref(conversation), ctypes.byref(handle))
    if result == 0:
        result = pam.pam_open_session(handle, 0)
    env = {}
    if result == 0:
        for key in ("XDG_RUNTIME_DIR", "DBUS_SESSION_BUS_ADDRESS"):
            value = pam.pam_getenv(handle, key.encode())
            env[key] = value.decode() if value else None
    channel.sendall((json.dumps({"result": result, "env": env}) + "\n").encode())
    if result == 0:
        channel.recv(1)
        result = pam.pam_close_session(handle, 0)
        pam.pam_end(handle, result)
        channel.sendall((json.dumps({"closed": result}) + "\n").encode())
    os._exit(0)


class Session:
    def __init__(self, username="alice", succeeds=True):
        self.channel, child = socket.socketpair()
        self.channel.settimeout(12)
        self.pid = os.fork()
        if self.pid == 0:
            self.channel.close()
            try:
                pam_worker(child, username)
            except BaseException:
                traceback.print_exc()
                os._exit(1)
        child.close()
        self.stream = self.channel.makefile("rb")
        self.opened = json.loads(self.stream.readline())
        assert (self.opened["result"] == 0) == succeeds, self.opened
        if not succeeds:
            os.waitpid(self.pid, 0)
            self.dispose()

    def dispose(self):
        self.stream.close()
        self.channel.close()

    def close(self):
        self.channel.sendall(b"x")
        result = json.loads(self.stream.readline())
        assert result["closed"] == 0, result
        os.waitpid(self.pid, 0)
        self.dispose()

    def crash(self):
        os.kill(self.pid, signal.SIGKILL)
        os.waitpid(self.pid, 0)
        self.dispose()


def start_daemon(log, **kwargs):
    # Remove only a stale socket after a previous test daemon has exited.
    Path("/run/turnstiled/control.sock").unlink(missing_ok=True)
    return subprocess.Popen(["/usr/bin/turnstiled"], stdout=log, stderr=log, **kwargs)


def check_readiness(log):
    reader, writer = os.pipe()
    env = dict(os.environ, TURNSTILED_READY_FD=str(writer))
    daemon = start_daemon(log, env=env, pass_fds=(writer,))
    os.close(writer)
    try:
        assert select.select([reader], [], [], 8)[0], "no readiness notification"
        assert os.read(reader, 1) == b"\n", "missing readiness byte"
        assert Path("/run/turnstiled/control.sock").is_socket()
        assert select.select([reader], [], [], 8)[0], "readiness fd was not closed"
        assert os.read(reader, 1) == b"", "extra readiness data"
        session = Session()  # No readiness polling/retry before this PAM call.
        session.close()
        wait_for(lambda: not Path("/run/user/1000").exists(), "readiness test cleanup")
        print("PASS: readiness byte, descriptor close, and immediate PAM login", flush=True)
    finally:
        os.close(reader)
        if daemon.poll() is None:
            daemon.terminate()
        daemon.wait(timeout=8)

    for value in ("", "2", "-1", "not-a-fd", "3x", "99999999999999999999999", "3"):
        # No descriptors are passed: even numeric fd 3 must fail validation.
        daemon = start_daemon(log, env=dict(os.environ, TURNSTILED_READY_FD=value))
        assert daemon.wait(timeout=8) != 0, ("invalid readiness fd accepted", value)
    print("PASS: invalid/closed readiness descriptors reject startup", flush=True)

    # Force initialization to fail before socket setup; never notify readiness.
    os.rename("/run", "/saved-run")
    Path("/run").write_text("not a directory\n")
    reader, writer = os.pipe()
    try:
        daemon = subprocess.Popen(
            ["/usr/bin/turnstiled"], stdout=log, stderr=log,
            env=dict(os.environ, TURNSTILED_READY_FD=str(writer)), pass_fds=(writer,))
        os.close(writer)
        assert daemon.wait(timeout=8) != 0
        assert select.select([reader], [], [], 8)[0]
        assert os.read(reader, 1) == b"", "startup failure signalled ready"
    finally:
        os.close(reader)
        Path("/run").unlink()
        os.rename("/saved-run", "/run")
    print("PASS: initialization failure never signals readiness", flush=True)

    reader, writer = os.pipe()
    os.close(reader)
    try:
        daemon = start_daemon(
            log, env=dict(os.environ, TURNSTILED_READY_FD=str(writer)), pass_fds=(writer,))
        assert daemon.wait(timeout=8) != 0, "broken readiness pipe accepted"
    finally:
        os.close(writer)
    print("PASS: disconnected readiness reader fails startup", flush=True)


def check_native_dinit(log):
    manager = subprocess.Popen(
        ["/bin/dinit", "--user", "-d", "/etc/dinit-test", "-p", "/run/test-dinitctl", "probe"],
        stdout=log, stderr=log)
    try:
        wait_for(lambda: Path("/run/probe-ready").exists(), "dependent dinit service")
        for service in ("turnstiled", "probe"):
            subprocess.run(["/bin/dinitctl", "-p", "/run/test-dinitctl", "is-started", service],
                           check=True, stdout=log, stderr=log, timeout=8)
        session = Session()
        session.close()
        wait_for(lambda: not Path("/run/user/1000").exists(), "dinit session cleanup")
        print("PASS: Mere-generated service readiness gates a native dinit dependent", flush=True)
    finally:
        if manager.poll() is None:
            subprocess.run(["/bin/dinitctl", "-p", "/run/test-dinitctl", "shutdown"],
                           check=True, stdout=log, stderr=log, timeout=8)
        manager.wait(timeout=8)


def check_user_backend(log):
    configuration = Path("/etc/turnstile/turnstiled.conf")
    original = configuration.read_text()
    configuration.write_text(original.replace("backend = none\n", "backend = dinit\n"))
    daemon = start_daemon(log)
    try:
        wait_for(lambda: Path("/run/turnstiled/control.sock").is_socket(), "user-backend daemon")
        first = Session()
        marker = Path("/run/user/1000/probe.pid")
        wait_for(lambda: marker.exists() and marker.read_text().strip(), "supervised user service")
        pid = int(marker.read_text())
        assert marker.stat().st_uid == 1000
        # Verify the supervised process, not just the marker, runs unprivileged.
        credentials = Path(f"/proc/{pid}/status").read_text()
        uid_line = next(line for line in credentials.splitlines() if line.startswith("Uid:"))
        assert uid_line.split()[1:] == ["1000"] * 4, uid_line
        print("PASS: dinit user backend starts a service as the logged-in UID", flush=True)
        second = Session()
        assert int(marker.read_text()) == pid
        first.close()
        os.kill(pid, 0)
        assert int(marker.read_text()) == pid
        print("PASS: concurrent logins share the same supervised user service", flush=True)
        os.kill(pid, signal.SIGKILL)
        wait_for(lambda: marker.exists() and marker.read_text().strip()
                 and int(marker.read_text()) != pid, "user service restart")
        restarted_pid = int(marker.read_text())
        os.kill(restarted_pid, 0)
        print("PASS: dinit restarts a crashed user service", flush=True)
        second.close()
        wait_for(lambda: not Path("/run/user/1000").exists(), "user-backend final logout")
        wait_for(lambda: not Path(f"/proc/{restarted_pid}").exists(), "user service termination")
        print("PASS: last logout stops user services and removes runtime directory", flush=True)
    finally:
        if daemon.poll() is None:
            daemon.terminate()
        daemon.wait(timeout=8)
        configuration.write_text(original)


def run_tests():
    log = open("/tmp/turnstiled.log", "w+")
    daemon = None
    try:
        check_readiness(log)
        daemon = start_daemon(log)
        wait_for(lambda: Path("/run/turnstiled/control.sock").is_socket(),
                 "daemon control socket")
        first = Session()
        assert first.opened["env"] == {
            "XDG_RUNTIME_DIR": "/run/user/1000", "DBUS_SESSION_BUS_ADDRESS": None
        }, first.opened
        directory = Path("/run/user/1000")
        info = directory.stat()
        assert (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) == (1000, 1000, 0o700)
        print("PASS: PAM environment, UID/GID and mode 0700", flush=True)

        marker = directory / "keep"
        marker.write_text("another login still needs this\n")
        second = Session()
        assert second.opened["env"] == first.opened["env"]
        first.close()
        time.sleep(0.2)
        assert marker.exists()
        print("PASS: concurrent login survives another login closing", flush=True)
        second.close()
        wait_for(lambda: not directory.exists(), "last-login cleanup")
        print("PASS: last logout removes directory and contents", flush=True)

        again = Session()
        assert not marker.exists()
        again.close()
        wait_for(lambda: not directory.exists(), "repeat login cleanup")
        print("PASS: repeated login/logout", flush=True)

        crashed = Session()
        crashed.crash()
        wait_for(lambda: not directory.exists(), "abrupt PAM-worker exit cleanup")
        print("PASS: abrupt PAM-worker exit cleanup", flush=True)

        user = Session()
        greeter = Session("greeter")
        assert greeter.opened["env"]["XDG_RUNTIME_DIR"] == "/run/user/1001"
        info = Path("/run/user/1001").stat()
        assert (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) == (1001, 1001, 0o700)
        greeter.close()
        wait_for(lambda: not Path("/run/user/1001").exists(), "greeter cleanup")
        assert directory.exists()
        user.close()
        wait_for(lambda: not directory.exists(), "user cleanup")
        print("PASS: distinct greeter/user runtime lifetimes", flush=True)

        # An existing directory must be normalized, not trusted as-is.
        directory.mkdir(mode=0o777)
        os.chmod(directory, 0o777)
        os.chown(directory, 1001, 1001)
        repaired = Session()
        info = directory.stat()
        assert (info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode)) == (1000, 1000, 0o700)
        repaired.close()
        wait_for(lambda: not directory.exists(), "repaired directory cleanup")
        print("PASS: existing directory ownership/mode normalized", flush=True)

        protected = Path("/tmp/protected")
        protected.mkdir()
        sentinel = protected / "sentinel"
        sentinel.write_text("must survive runtime cleanup\n")
        linked = Session()
        (directory / "outside").symlink_to(protected, target_is_directory=True)
        linked.close()
        wait_for(lambda: not directory.exists(), "directory with symlink cleanup")
        assert sentinel.read_text() == "must survive runtime cleanup\n"
        print("PASS: cleanup does not follow a symlink in runtime contents", flush=True)

        directory.symlink_to(protected, target_is_directory=True)
        Session(succeeds=False)
        assert sentinel.read_text() == "must survive runtime cleanup\n"
        assert directory.is_symlink()
        directory.unlink()
        print("PASS: symlink in place of runtime directory rejected", flush=True)

        live = Session()
        daemon.terminate()
        daemon.wait(timeout=8)
        wait_for(lambda: not directory.exists(), "provider shutdown cleanup")
        os.kill(live.pid, 0)  # The PAM caller still exists, but is no longer tracked.
        live.close()
        print("NOTE: stopping the provider removes runtime dirs even with a live PAM caller; "
              "do not restart it during active sessions", flush=True)
        Session(succeeds=False)
        print("PASS: provider unavailable returns a PAM error", flush=True)
        check_native_dinit(log)
        check_user_backend(log)
    finally:
        if daemon is not None and daemon.poll() is None:
            daemon.terminate()
            daemon.wait(timeout=8)
        log.flush()
        log.seek(0)
        print("\nDaemon output:\n" + log.read(), flush=True)
        log.close()


def run_isolated(populate_root, run_suite, prefix="turnstile-session-test-"):
    if os.geteuid() != 0:
        raise PermissionError("requires root for isolated namespaces and chroot")
    libc = ctypes.CDLL(None, use_errno=True)
    libc.unshare.argtypes = [ctypes.c_int]
    libc.mount.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p,
                           ctypes.c_ulong, ctypes.c_void_p]
    with tempfile.TemporaryDirectory(prefix=prefix) as temp:
        root = Path(temp)
        populate_root(root)
        # Private mounts and PID namespace: exiting its PID 1 kills all helpers,
        # including children that create their own process groups/sessions.
        if libc.unshare(0x00020000 | 0x20000000) != 0:
            raise OSError(ctypes.get_errno(), "unshare mount/PID namespaces")
        if libc.mount(None, b"/", None, (1 << 14) | (1 << 18), None) != 0:
            raise OSError(ctypes.get_errno(), "make mounts recursively private")
        pid = os.fork()
        if pid == 0:
            try:
                libc.prctl(1, signal.SIGKILL, 0, 0, 0)  # PR_SET_PDEATHSIG
                if libc.mount(b"proc", os.fsencode(root / "proc"), b"proc", 0, None) != 0:
                    raise OSError(ctypes.get_errno(), "mount private procfs")
                os.chroot(root)
                os.chdir("/")
                run_suite()
                os._exit(0)
            except BaseException:
                traceback.print_exc()
                os._exit(1)
        _, status = os.waitpid(pid, 0)
        # procfs was mounted in this namespace, but only viewed from the child.
        if libc.umount2(os.fsencode(root / "proc"), 2) != 0:
            raise OSError(ctypes.get_errno(), "unmount private procfs")
        return os.waitstatus_to_exitcode(status)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("staging", type=Path)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error("requires root for isolated namespaces and chroot")
    package = args.staging.resolve()
    return run_isolated(lambda root: populate(root, package), run_tests)


if __name__ == "__main__":
    sys.exit(main())
