#!/usr/bin/env python3
"""Test staged greetd and Turnstile packages without touching host PAM or VTs.

Run as root:
  python3 test/greetd/session-integration.py GREETD_STAGING TURNSTILE_STAGING

Requires the same host runtime libraries and dinit/BusyBox tools as the Turnstile
lifecycle test. Uses a disposable chroot in private mount and PID namespaces.
"""
import argparse
import ctypes
import importlib.util
import json
import os
from pathlib import Path
import shutil
import signal
import socket
import struct
import subprocess
import sys
import time
import tomllib

# Reuse namespace isolation and the minimal runtime filesystem fixtures.
sys.dont_write_bytecode = True
helper_path = Path(__file__).resolve().parents[1] / "turnstile/session-lifecycle.py"
spec = importlib.util.spec_from_file_location("turnstile_test", helper_path)
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)

PASSWORD = "disposable-test-password"


def populate(root, greetd, turnstile):
    helper.populate(root, turnstile)
    (root / "usr/sbin").mkdir()
    shutil.copy2("/usr/sbin/unix_chkpwd", root / "usr/sbin/unix_chkpwd")
    for program in ("greetd", "agreety"):
        shutil.copy2(greetd / "usr/bin" / program, root / "usr/bin" / program)
    shutil.copytree(greetd / "etc-defaults", root / "etc", dirs_exist_ok=True)
    shutil.copy2(greetd / "usr/share/dinit.d/greetd", root / "etc/dinit-test/greetd")
    policies = Path(__file__).resolve().parents[2] / "recipes/core/linux-pam"
    for policy in ("system-auth", "system-account", "system-password", "system-session"):
        shutil.copy2(policies / policy, root / "etc/pam.d" / policy)
    for name in ("pam_env.conf", "access.conf"):
        (root / "etc/security" / name).write_text("")
    (root / "etc/environment").write_text("PATH=/bin:/usr/bin\n")
    # Fixture credentials only; no host account/password data are copied.
    crypt = ctypes.CDLL("/usr/lib/libcrypt.so.1")
    crypt.crypt.argtypes = [ctypes.c_char_p, ctypes.c_char_p]
    crypt.crypt.restype = ctypes.c_char_p
    password_hash = crypt.crypt(PASSWORD.encode(), b"$6$greetdtest$")
    assert password_hash and password_hash.startswith(b"$6$")
    day = int(time.time() // 86400)
    (root / "etc/shadow").write_text(
        f"root:!:{day}:0:99999:7:::\n"
        f"alice:{password_hash.decode()}:{day}:0:99999:7:::\n"
        f"greeter:!:{day}:0:99999:7:::\n")
    os.chmod(root / "etc/shadow", 0o600)
    shutil.copy2("/bin/id", root / "bin/id")
    (root / "usr/bin/test-greeter").write_text(
        "printf '%s\\n' \"$$\" > \"$XDG_RUNTIME_DIR/greeter.pid\"\n"
        "exec /bin/sleep 300\n")
    (root / "usr/bin/test-session").write_text(
        "printf '%s\\n' \"$XDG_RUNTIME_DIR\" \"$HOME\" \"$USER\" "
        "\"$XDG_SESSION_TYPE\" > \"$HOME/session.env\"\n"
        "/bin/id -u > \"$HOME/session.uid\"\n"
        "printf '%s\\n' \"$$\" > \"$HOME/session.pid\"\n"
        "exec /bin/sleep 300\n")
    configuration = root / "etc/greetd/config.toml"
    text = configuration.read_text()
    defaults = tomllib.loads(text)
    assert defaults["terminal"]["vt"] == 7
    assert defaults["default_session"]["user"] == "greeter"
    assert defaults["default_session"]["command"] == "/usr/bin/agreety --cmd /bin/sh"
    assert "initial_session" not in defaults
    # No real terminal is opened, switched or attached in this suite.
    text = text.replace("vt = 7", 'vt = "none"').replace("switch = true", "switch = false")
    text = text.replace('command = "/usr/bin/agreety --cmd /bin/sh"',
                        'command = "/bin/sh /usr/bin/test-greeter"')
    configuration.write_text(text)


def receive_exact(channel, size):
    data = b""
    while len(data) < size:
        part = channel.recv(size - len(data))
        if not part:
            raise AssertionError("greetd closed the IPC connection")
        data += part
    return data


def request(channel, message):
    payload = json.dumps(message).encode()
    channel.sendall(struct.pack("=I", len(payload)) + payload)
    length, = struct.unpack("=I", receive_exact(channel, 4))
    assert length < 1024 * 1024
    return json.loads(receive_exact(channel, length))


def authenticate(channel, password):
    response = request(channel, {"type": "create_session", "username": "alice"})
    for _ in range(8):
        if response["type"] != "auth_message":
            return response
        # This suite uses the known pam_unix fixture, not arbitrary PAM/MFA.
        answer = password if response["auth_message_type"] == "secret" else None
        response = request(channel, {"type": "post_auth_message_response", "response": answer})
    raise AssertionError("too many PAM messages")


def connect():
    paths = list(Path("/run").glob("greetd-*.sock"))
    assert len(paths) == 1, paths
    channel = socket.socket(socket.AF_UNIX)
    channel.settimeout(15)
    channel.connect(str(paths[0]))
    return channel


def runtime_info(uid):
    info = Path(f"/run/user/{uid}").stat()
    assert (info.st_uid, info.st_gid, info.st_mode & 0o777) == (uid, uid, 0o700)


def run_tests():
    log = open("/tmp/greetd-integration.log", "w+")
    manager = subprocess.Popen(
        ["/bin/dinit", "--user", "-d", "/etc/dinit-test", "-p", "/run/test-dinitctl", "greetd"],
        stdout=log, stderr=log)
    try:
        greeter_pid_file = Path("/run/user/1001/greeter.pid")
        helper.wait_for(lambda: greeter_pid_file.exists() and greeter_pid_file.read_text().strip(),
                        "greetd greeter session", timeout=15)
        runtime_info(1001)
        assert greeter_pid_file.stat().st_uid == 1001
        old_greeter_pid = int(greeter_pid_file.read_text())
        print("PASS: generated dinit graph starts Turnstile before greetd's PAM session", flush=True)
        print("PASS: locked greeter account gets its own private runtime directory", flush=True)

        with connect() as channel:
            response = authenticate(channel, "incorrect-password")
            assert response["type"] == "error" and response["error_type"] == "auth_error", response
            request(channel, {"type": "cancel_session"})
        assert not Path("/home/alice/session.pid").exists()
        assert not Path("/run/user/1000").exists()
        print("PASS: incorrect password does not create a user session", flush=True)

        with connect() as channel:
            response = authenticate(channel, PASSWORD)
            assert response["type"] == "success", response
            response = request(channel, {
                "type": "start_session", "cmd": ["/bin/sh /usr/bin/test-session"],
                "env": ["XDG_SESSION_TYPE=wayland"],
            })
            assert response["type"] == "success", response
        # A real greeter exits after StartSession succeeds; emulate that here.
        os.kill(old_greeter_pid, signal.SIGTERM)
        user_pid_file = Path("/home/alice/session.pid")
        helper.wait_for(lambda: user_pid_file.exists() and user_pid_file.read_text().strip(),
                        "authenticated user command", timeout=15)
        runtime_info(1000)
        assert Path("/home/alice/session.uid").read_text().strip() == "1000"
        assert Path("/home/alice/session.env").read_text().splitlines() == [
            "/run/user/1000", "/home/alice", "alice", "wayland"]
        print("PASS: real pam_unix authentication launches a command as UID 1000", flush=True)
        print("PASS: greetd propagates Turnstile's PAM environment into the user command", flush=True)
        helper.wait_for(lambda: not Path("/run/user/1001").exists(), "previous greeter cleanup")
        assert Path("/run/user/1000").exists()
        print("PASS: greeter cleanup leaves the user's runtime directory intact", flush=True)

        os.kill(int(user_pid_file.read_text()), signal.SIGTERM)
        helper.wait_for(lambda: not Path("/run/user/1000").exists(), "user logout cleanup")
        helper.wait_for(lambda: greeter_pid_file.exists() and greeter_pid_file.read_text().strip()
                        and int(greeter_pid_file.read_text()) != old_greeter_pid,
                        "greeter return", timeout=15)
        runtime_info(1001)
        print("PASS: user logout cleans runtime state and returns to a fresh greeter", flush=True)

        subprocess.run(["/bin/dinitctl", "-p", "/run/test-dinitctl", "shutdown"],
                       check=True, stdout=log, stderr=log, timeout=8)
        manager.wait(timeout=10)
        helper.wait_for(lambda: not Path("/run/user/1001").exists(), "final greeter cleanup")
        print("PASS: dependency-ordered shutdown cleans the remaining greeter session", flush=True)

        # The required session provider must fail closed, without a runtime-dir fallback.
        result = subprocess.run(["/usr/bin/greetd", "--config", "/etc/greetd/config.toml"],
                                stdout=log, stderr=log, timeout=12)
        assert result.returncode != 0
        assert not Path("/run/user/1001").exists()
        print("PASS: missing Turnstile prevents greeter session startup", flush=True)

        passwd = Path("/etc/passwd")
        original = passwd.read_text()
        try:
            passwd.write_text("\n".join(line for line in original.splitlines()
                                        if not line.startswith("greeter:")) + "\n")
            result = subprocess.run(["/usr/bin/greetd", "--config", "/etc/greetd/config.toml"],
                                    stdout=log, stderr=log, timeout=12)
            assert result.returncode != 0
            print("PASS: missing greeter account is rejected, not silently provisioned", flush=True)
        finally:
            passwd.write_text(original)
    finally:
        if manager.poll() is None:
            subprocess.run(["/bin/dinitctl", "-p", "/run/test-dinitctl", "shutdown"],
                           stdout=log, stderr=log, timeout=8)
            manager.wait(timeout=10)
        log.flush()
        log.seek(0)
        print("\nManager output:\n" + log.read(), flush=True)
        log.close()
        for path in ("/var/log/greetd.log", "/var/log/turnstiled.log"):
            if Path(path).exists():
                print(f"\n{path}:\n" + Path(path).read_text(), flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("greetd_staging", type=Path)
    parser.add_argument("turnstile_staging", type=Path)
    args = parser.parse_args()
    if os.geteuid() != 0:
        parser.error("requires root for isolated namespaces and chroot")
    greetd = args.greetd_staging.resolve()
    turnstile = args.turnstile_staging.resolve()
    return helper.run_isolated(lambda root: populate(root, greetd, turnstile),
                               run_tests, prefix="greetd-session-test-")


if __name__ == "__main__":
    sys.exit(main())
