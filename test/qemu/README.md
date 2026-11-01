# QEMU guest tests

This directory contains developer test tooling, not an installer or a supported
end-user image format. The first probe establishes whether software-emulated
Linux can provide the namespace operations needed by Mere. It does not test Mere
builds, dinit, disk-backed boot, or a bootloader.

## Namespace smoke test

Host dependencies:

- A POSIX shell, `mktemp`, `cpio` with `newc` output, `gzip`, `timeout`, and common
  POSIX utilities. The shell syntax is POSIX; not all external tools are POSIX.
- `qemu-system-x86_64` with TCG, PC firmware, and serial-console support.
- An x86_64 Linux kernel supporting initramfs, serial console, user/mount/PID
  namespaces, procfs, sysfs, devtmpfs, and tmpfs, with those facilities built in.
- A static BusyBox with `sh`, `--install`, `mount`, `umount`, `unshare` (including
  user mapping and fork options), `cat`, `uname`, `sync`, and `poweroff`.

Run from the repository root:

```sh
sh test/qemu/namespace-smoke /absolute/path/to/vmlinuz /absolute/path/to/busybox
```

The inputs must be supplied explicitly; the script does not download or install
host software. Keep their versions and checksums with any reported test result.
An Ubuntu 6.8.0-138-generic kernel, Ubuntu static BusyBox 1.36.1, and QEMU 8.2.2
were used for the initial successful run. These are test inputs, not a distro
kernel or userspace decision.

The script creates a disposable initramfs, starts QEMU with software emulation,
and prints the guest serial log. No host root privileges, loop devices, mounts,
KVM, networking, or writable guest disk are required.

The guest checks that it can:

1. Boot Linux and run the probe as init.
2. Enter new user, mount, and PID namespaces and map its user/group to root.
3. Run as PID 1 and mount a private procfs showing only the namespace's init.
4. Mount, write/read, and unmount a tmpfs.
5. Report `NAMESPACE_PROBE_PASS` and power off.

The launcher returns success only when QEMU exits successfully and the pass marker
is present. Kernel panics, failed probes, missing inputs, and timeouts produce a
nonzero exit status. Temporary files are removed on exit; redirect output to keep
the serial log. The default timeout is 120 seconds:

```sh
QEMU_TIMEOUT=180 sh test/qemu/namespace-smoke "$kernel" "$busybox" > guest.log 2>&1
```

Set `QEMU` to an executable wrapper if your QEMU needs firmware or module paths.
The value is one executable path, not a shell command with arguments. For example,
a wrapper can set `QEMU_MODULE_DIR`, then use `exec qemu-system-x86_64` with `-L`
and `-bios` arguments followed by `"$@"`. No machine-specific paths are baked
into the harness.

## Next steps

Track harness work in jhuntwork/merelinux#635, distro boot work in #634, and the
overall dinit transition in #633. A Mere disk-backed guest without an initramfs
is a separate next step. Extend guest scenarios for package-manager execution and
service behavior rather than treating this environment probe as that evidence.

## Disk-backed Mere/dinit smoke test

`dinit-smoke` copies an existing named profile and its store into a disposable
ext4 image. It boots the profile's own `boot/vmlinux`, runs dinit directly as
PID 1, verifies the mounted root and PID 1 identity, then requests power-off
through dinit. It supplies a minimal test-only service graph. It does not install
or select the distro's production boot services, verify a bootloader, or test
package-manager service reconciliation.

Prepare an alternate storage root with the official repository config and key,
then install the three test inputs:

```sh
mere --root "$storage" install -p guest linux busybox dinit
QEMU_TIMEOUT=120 sh test/qemu/dinit-smoke "$storage" guest > dinit-guest.log 2>&1
```

The prepared root must have a named profile with logical `/mere/store` links and
`boot/vmlinux`, `/bin/dinit`, `/bin/sh`, mount utilities, and dinit's `shutdown`.
Use a dedicated test profile. Its `etc-defaults` are deliberately not activated:
the harness supplies its own boot, probe, and shutdown services under `/etc`.

Additional host dependencies are `readlink`, `truncate`, and `mke2fs` supporting
`-d` directory population. No host mounts or loop devices are used. The kernel
must have ext4, IDE/ATA disk support, serial console, and automatic devtmpfs
mounting built in. QEMU loads the kernel directly with `root=/dev/sda` and
`init=/bin/dinit`; no initramfs is passed.

`QEMU` and `QEMU_TIMEOUT` work as above. `QEMU_DISK_SIZE` defaults to `384M` and
must accommodate the copied store. The launcher reports success only after the
boot marker, dinit's kernel shutdown message, and kernel power-off message appear
and QEMU exits successfully. The copied root and disk are removed afterward.

The initial successful inputs were Mere linux 6.18.42-2, BusyBox 1.37.0-10, and
dinit 0.22.1-1 (x86_64), with QEMU 8.2.2 TCG. Dinit stopped the test services and
powered the guest off. The test does not establish complete filesystem shutdown
ordering or persistent-disk integrity; those need explicit boot/shutdown services
and further checks under #634. These input versions describe observed evidence,
not a frozen dependency set.
