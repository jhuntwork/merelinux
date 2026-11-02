#!/usr/bin/env python3
"""Disposable, offline QEMU checks of the published Mere boot contract."""
import hashlib
import math
import os
from pathlib import Path
import re
import selectors
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
PASSWORD = "mere-guest-test"  # Public fixture credential; never use on a real system.
PACKAGES = {"linux", "busybox", "dinit", "shadow", "mdevd", "mere-boot"}


def run(args, log=None, **kwargs):
    return subprocess.run(args, check=True, stdout=log, stderr=log, **kwargs)


def write(root, name, text, mode=0o644):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)
    path.chmod(mode)


def fsck(disk, log):
    # -n never repairs: even a repairable inconsistency fails the scenario.
    with log.open("wb") as output:
        run(["e2fsck", "-fn", str(disk)], output)


def dialogue(qemu, kernel, disk, case, output, timeout):
    command = [qemu, "-accel", "tcg,thread=single", "-m", "512", "-smp", "1",
               "-nodefaults", "-display", "none", "-serial", "stdio", "-monitor", "none",
               "-nic", "none", "-kernel", str(kernel), "-drive",
               f"file={disk},format=raw,if=ide", "-append",
               "console=ttyS0 root=/dev/sda rootfstype=ext4 ro init=/sbin/init panic=-1"]
    if case not in ("reboot", "lifecycle"):
        command += ["-no-reboot"]
    with output.open("wb") as log, subprocess.Popen(
            command, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT) as proc:
        selector = selectors.DefaultSelector()
        selector.register(proc.stdout, selectors.EVENT_READ)
        transcript = b""
        pending = b""
        stage = "menu" if case == "recovery" else "login"
        cycle = 0
        wrong_sent = False
        deadline = time.monotonic() + timeout

        def send(text):
            proc.stdin.write(text.encode())
            proc.stdin.flush()

        try:
            while True:
                if time.monotonic() > deadline:
                    raise RuntimeError(f"{case}: timed out in {stage}")
                for key, _ in selector.select(0.2):
                    chunk = os.read(key.fd, 65536)
                    if not chunk:
                        selector.unregister(key.fileobj)
                        continue
                    log.write(chunk)
                    log.flush()
                    transcript += chunk
                    pending += chunk
                if case != "recovery" and stage != "shutdown" and b"(p)ower off? " in pending:
                    send("p")
                    stage = "shutdown"
                # Consume only up to each prompt so coalesced output is preserved.
                while True:
                    if stage == "menu":
                        prompt = b"(p)ower off? "
                    elif stage == "password":
                        prompt = b"Password:"
                    elif stage in ("login", "retry"):
                        prompt = b"login:"
                    elif stage == "shell":
                        # Root's default shell prompt from the packaged login/profile.
                        prompt = b"# "
                    else:
                        break
                    pos = pending.find(prompt)
                    if pos < 0:
                        break
                    consumed = pending[:pos + len(prompt)]
                    pending = pending[pos + len(prompt):]
                    if stage == "menu":
                        if b"Password:" in consumed:
                            raise RuntimeError("Recovery login began before menu selection")
                        send("e")
                        stage = "password"
                    elif stage in ("login", "retry"):
                        if stage == "retry" and b"Login incorrect" not in consumed:
                            raise RuntimeError("Wrong recovery password was not rejected")
                        send("root\n")
                        stage = "password"
                    elif stage == "password":
                        if case == "recovery" and not wrong_sent:
                            send("incorrect-guest-password\n")
                            wrong_sent = True
                            stage = "retry"
                        else:
                            send(PASSWORD + "\n")
                            stage = "shell"
                    elif stage == "shell":
                        if case == "recovery":
                            send("[ \"$(id -u)\" = 0 ] && dinitctl list >/dev/null && "
                                 "printf 'PACKAGED_%s_PASS\\n' RECOVERY && /sbin/shutdown -p\n")
                            stage = "shutdown"
                        elif case == "lifecycle":
                            send(f"/bin/sh /etc/lifecycle/run {cycle}\n")
                            stage = "login" if cycle < 2 else "shutdown"
                            cycle += 1
                        elif case == "reboot" and cycle == 0:
                            send("/bin/sh /etc/boot-test/check && "
                                 "printf 'persistent-data\\n' > /var/log/boot-test-data && "
                                 "sync && /sbin/shutdown -r\n")
                            cycle = 1
                            stage = "login"
                        else:
                            check = "/bin/sh /etc/boot-test/check && "
                            if case == "reboot":
                                check += ("grep -qx persistent-data /var/log/boot-test-data && "
                                          "grep -qx mounts-present /var/log/boot-test-stops && "
                                          "printf 'PACKAGED_%s_PASS\\n' REBOOT && ")
                            send(check + "/sbin/shutdown -p\n")
                            stage = "shutdown"
                if not selector.get_map() and proc.poll() is not None:
                    break
            if proc.wait() != 0:
                raise RuntimeError(f"{case}: QEMU exited {proc.returncode}")
        finally:
            selector.close()
            if proc.poll() is None:
                proc.kill()
                proc.wait()
        text = transcript.decode(errors="replace")
        required = ["Issuing shutdown via kernel", "reboot: Power down"]
        if case == "recovery":
            required += ["PACKAGED_RECOVERY_PASS", "Login incorrect", "does-not-exist"]
            if text.count("(p)ower off? ") != 1 or "reboot: Restarting system" in text:
                raise RuntimeError("Recovery must use exactly one menu and never reboot")
            if "PACKAGED_BOOT_PASS" in text:
                raise RuntimeError("Failed boot reported normal boot completion")
        else:
            required += ["PACKAGED_BOOT_PASS"]
            if "(p)ower off? " in text:
                raise RuntimeError(f"{case}: unexpected boot failure menu")
        if case == "reboot":
            required += ["PACKAGED_REBOOT_PASS", "reboot: Restarting system"]
            if text.count("PACKAGED_BOOT_PASS") != 2:
                raise RuntimeError("Reboot must pass both boot cycles")
        if case == "lifecycle":
            failed = re.search(r"LIFECYCLE_PHASE_[0-2]_FAIL", text)
            if failed:
                raise RuntimeError(f"Lifecycle guest reported {failed.group()}; see serial.log")
            required += ["MERE_PACKAGE_LIFECYCLE_PASS", "MERE_SERVICE_LIFECYCLE_PASS",
                         "MERE_ENABLED_BOOT_PASS", "MERE_DISABLED_BOOT_PASS"]
            required += [f"LIFECYCLE_PHASE_{phase}_PASS" for phase in range(3)]
            if text.count("PACKAGED_BOOT_PASS") != 3 or text.count("reboot: Restarting system") != 2:
                raise RuntimeError("Lifecycle checks require three successful boot cycles")
        for marker in required:
            if marker not in text:
                raise RuntimeError(f"{case}: missing {marker}")


def main():
    if len(sys.argv) not in (3, 4):
        raise RuntimeError("Usage: packaged-boot-smoke ABSOLUTE_MERE NEW_ABSOLUTE_RESULTS [PREVIOUS_INPUTS]")
    mere, results = Path(sys.argv[1]), Path(sys.argv[2])
    if not mere.is_absolute() or not results.is_absolute():
        raise RuntimeError("Mere and results paths must be absolute")
    if os.uname().machine != "x86_64":
        raise RuntimeError("This launcher requires an x86_64 host and packages")
    lifecycle = os.environ.get("MERE_LIFECYCLE_TESTS") == "1"
    qemu = os.environ.get("QEMU", "qemu-system-x86_64")
    for tool in (qemu, "sh", "curl", "sha256sum", "uname", "mke2fs", "e2fsck", "debugfs", "openssl"):
        if not shutil.which(tool):
            raise RuntimeError(f"Missing host utility: {tool}")
    if lifecycle and not shutil.which("readelf"):
        raise RuntimeError("Missing host utility: readelf")
    timeout = float(os.environ.get("QEMU_TIMEOUT", "600" if lifecycle else "180"))
    if not math.isfinite(timeout) or timeout <= 0:
        raise RuntimeError("QEMU_TIMEOUT must be finite and positive")
    disk_mib = int(os.environ.get("QEMU_DISK_MIB", "512"))
    if disk_mib <= 0:
        raise RuntimeError("QEMU_DISK_MIB must be positive")
    results.mkdir()  # Refuse stale logs/markers or existing package state.
    with tempfile.TemporaryDirectory(prefix="mere-packaged-boot-") as work_dir:
        root = Path(work_dir) / "root"
        try:
            args = ["sh", str(HERE / "prepare-root"), str(mere), str(root)] + sys.argv[3:]
            with (results / "setup.log").open("wb") as output:
                run(args, output, env={**os.environ, "MERE_BOOT_TESTS": "1"})
            shutil.move(str(root / "test-inputs"), results / "inputs")
            inputs = results / "inputs"
            profile = (inputs / "profile.kdl").read_text()
            if not PACKAGES.issubset(set(re.findall(r'package "([^"]+)"', profile))):
                raise RuntimeError("Recorded profile lacks required boot packages")
            # Keep root directory views tied to the active system generation.
            for name in ("bin", "sbin", "usr", "lib"):
                (root / name).symlink_to(f"/mere/profiles/system/current/{name}")
            kernel = root / "mere/profiles/system/current/boot/vmlinux"
            target = os.readlink(kernel)
            if not target.startswith("/mere/store/"):
                raise RuntimeError("Expected packaged kernel store link")
            kernel = root / target.lstrip("/")
            for name in ("proc", "sys", "dev", "run", "tmp", "root", "home", "mnt/test", "var/log"):
                (root / name).mkdir(parents=True, exist_ok=True)
            password_hash = subprocess.check_output(
                ["openssl", "passwd", "-6", "-salt", "mereboot", "-stdin"],
                input=(PASSWORD + "\n").encode()).decode().strip()
            write(root, "etc/passwd", "root:x:0:0:Test root:/root:/bin/sh\n")
            write(root, "etc/group", (HERE / "boot-fixtures/group").read_text())
            write(root, "etc/shadow", f"root:{password_hash}:19000:0:99999:7:::\n", 0o600)
            write(root, "etc/hostname", "mere-boot-test\n")
            for source in (HERE / "boot-fixtures").iterdir():
                write(root, "etc/boot-test/" + source.name, source.read_text())
            write(root, "etc/dinit.d/boot-test-lifetime",
                  "type = scripted\ncommand = /bin/true\n"
                  "stop-command = /bin/sh /etc/boot-test/lifetime\ndepends-on = sysinit\n")
            (root / "etc/dinit.d/boot.d/boot-test-lifetime").symlink_to("../boot-test-lifetime")
            (root / "etc/dinit.d/boot.d/ttyS0").symlink_to("/usr/share/dinit.d/ttyS0")
            shutil.copytree(HERE / "boot-fixtures", inputs / "boot-fixtures")
            shutil.copy2(__file__, inputs / "packaged-boot.py")
            shutil.copy2(HERE / "prepare-root", inputs / "prepare-root")
            (inputs / "qemu.version").write_bytes(subprocess.check_output([qemu, "--version"]))
            (inputs / "kernel.sha256").write_text(hashlib.sha256(kernel.read_bytes()).hexdigest() + "\n")
            if lifecycle:
                sys.dont_write_bytecode = True
                from lifecycle import prepare
                prepare(mere, root, inputs, HERE)
            cases = ("lifecycle",) if lifecycle else ("boot", "reboot", "recovery")
            for case in cases:
                case_dir = results / case
                case_dir.mkdir()
                fstab = "tmpfs /mnt/test tmpfs defaults 0 0\n"
                if case == "recovery":
                    fstab = "/dev/does-not-exist /mnt/test ext4 defaults 0 0\n"
                write(root, "etc/fstab", fstab)
                disk = Path(work_dir) / f"{case}.ext4"
                with disk.open("wb") as image:
                    image.truncate(disk_mib * 1024 * 1024)
                with (case_dir / "assemble.log").open("wb") as output:
                    run(["mke2fs", "-q", "-t", "ext4", "-F", "-d", str(root), str(disk)], output)
                fsck(disk, case_dir / "before.fsck")
                # Preserve a postmortem filesystem report even if dialogue fails.
                try:
                    dialogue(qemu, kernel, disk, case, case_dir / "serial.log", timeout)
                finally:
                    fsck(disk, case_dir / "after.fsck")
                stops = subprocess.check_output(
                    ["debugfs", "-R", "cat /var/log/boot-test-stops", str(disk)],
                    stderr=subprocess.DEVNULL).decode()
                (case_dir / "stop.log").write_text(stops)
                expected = {"recovery": 0, "reboot": 2, "lifecycle": 3}.get(case, 1)
                if stops.splitlines() != ["mounts-present"] * expected:
                    raise RuntimeError(f"{case}: service stop ordering evidence differs")
                disk.unlink()
                print(f"{case}: PASS", flush=True)
        finally:
            # Store directories can be read-only; do not follow logical symlinks.
            for directory, dirs, files in os.walk(root, followlinks=False):
                os.chmod(directory, os.stat(directory).st_mode | 0o700)
    print(f"Results: {results}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as error:
        print(f"packaged-boot: {error}", file=sys.stderr)
        sys.exit(1)
