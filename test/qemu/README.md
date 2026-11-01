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
overall dinit transition in #633. Disk boot and package-manager execution
are covered separately below; the namespace probe alone is not evidence for them.

## Disk-backed Mere/dinit smoke test

Run the complete preparation and boot flow with an explicit Mere binary and a
new results directory:

```sh
QEMU_TIMEOUT=120 sh test/qemu/dinit-smoke /absolute/path/to/mere \
    /absolute/new/results
```

The launcher creates a temporary root and calls `prepare-root` to download the
public configuration and key and install `linux`, `busybox`, and `dinit` into
profile `guest`. That same storage tree becomes the guest root: only the
profile's directory views are copied into place; the store is not copied into a
second staging tree. `mke2fs -d` populates a disposable ext4 disk directly from
that root. No host mounts, loop devices, KVM, or host namespaces are needed.

The supplied Mere binary must run on the host. Additional host tools are `curl`,
`sha256sum`, `readlink`, `truncate`, and `mke2fs` supporting directory population,
plus QEMU, `timeout`, and shell utilities. The launcher checks its assembly tools
before setup; `prepare-root` checks its own dependencies before downloading.
No host software is installed automatically.

The guest kernel must have ext4, IDE/ATA disk support, serial console, and
automatic devtmpfs mounting built in. QEMU loads the installed kernel directly
with `root=/dev/sda` and `init=/bin/dinit`; no initramfs is passed. The harness
supplies a minimal test-only service graph under `/etc`, verifies PID 1 and the
mounted root, then requests shutdown through dinit. Package `etc-defaults` are
not activated. Bootloader behavior, production boot services, shutdown ordering,
persistent-disk integrity, and package-manager service reconciliation remain
separate tests under #634.

The results directory must not already exist. It preserves `setup.log`,
`serial.log`, and `inputs/` outside the disposable root. Inputs include the Mere
version and SHA-256, host architecture, public configuration and key with hashes,
and resolved `profile.kdl` with package versions, releases, and content hashes.
The first run selects current published packages. Replay those identities with:

```sh
sh test/qemu/dinit-smoke /absolute/path/to/mere /absolute/new/replay-results \
    /absolute/previous/results/inputs
```

Replay requires the same Mere binary digest and host architecture and reuses the
recorded config and key. It still needs network access and repository retention
of the recorded packages and metadata; saved inputs are not an offline archive.
Initial configuration/key trust comes from HTTPS. Keep the recorded inputs with
reported results. A failed run retains available logs while deleting its
disposable root and disk. `QEMU_DISK_SIZE` defaults to `384M`; `QEMU` and
`QEMU_TIMEOUT` work as described above.

`prepare-root` can also be run separately for inspection:

```sh
sh test/qemu/prepare-root /absolute/path/to/mere /absolute/new/storage-root
```

It refuses an existing storage root, records inputs in `test-inputs/`, and accepts
a previous inputs directory as an optional third argument. Standalone setup
leaves its root in place, including partial state on failure. The combined boot
launcher always creates its own disposable root rather than reusing that state.

The initial successful disk-boot inputs were Mere linux 6.18.42-2, BusyBox
1.37.0-10, and dinit 0.22.1-1 (x86_64), with QEMU 8.2.2 TCG. These versions
record observed evidence rather than a frozen dependency set. The launcher
requires successful QEMU exit, the boot pass marker, dinit's kernel shutdown
message, and kernel power-off message. This remains developer tooling rather
than an end-user installer or production boot configuration.

## Offline Mere shell/build smoke test

```sh
QEMU_TIMEOUT=120 sh test/qemu/mere-smoke /absolute/path/to/static/mere \
    /absolute/new/mere-results
```

This extends `dinit-smoke` using the same preparation, image assembly, shutdown,
and cleanup flow. Supply an x86_64 static ELF Mere binary (the published binary
is suitable). The additional host dependency is `readelf` for recording ELF
program headers and rejecting an interpreter-dependent executable. Preparation
also needs `sed`. The guest profile adds `zstd` and its dependencies so the guest
can decompress and inspect its freshly built archive. Other host requirements
are the same as the disk smoke test.

Host preparation downloads packages and metadata. QEMU has no network device:
the guest uses a `file:///guest-repo` mirror assembled from the signed upstream
metadata and downloaded package cache. Only the transport URL changes; the
upstream key, fingerprint, and signature verification remain in use. This mirror
currently expects the single public Mere repository configuration. It is not a
networking test.

After checking dinit and disk boot, the guest:

1. Runs the supplied Mere binary and enters profile `guest` to execute a marker.
2. Generates a disposable development signing key in its own home directory.
3. Builds the local `recipes/probe` fixture through Mere's isolated build path.
4. Decompresses and extracts the resulting package, requiring exactly one archive
   and the expected `usr/share/guest-probe/result` payload (`guest-build`).
5. Builds `recipes/fail`, requiring Mere exit status 1, the recipe's exit code 7
   in its diagnostic, and no package archive from that failing build.
6. Reports success and powers off through dinit.

The host requires all scenario markers as well as the normal shutdown markers
and successful QEMU exit. A failed guest probe prevents normal shutdown and the
host timeout returns failure. `serial.log` preserves build output and the failure
diagnostic; `inputs/` also records ELF headers, the guest repository configuration,
metadata/archive hashes, and fixture sources. The generated private key, built
archive, and guest filesystem are disposable and are not retained.

Replay with a third argument pointing at a prior **mere-smoke** `inputs/`
directory. Replay from a plain dinit run lacks the required zstd package and is
rejected before boot. As with `dinit-smoke`, host replay still needs network
access and repository retention; guest execution is offline. The fixture tests
Mere shell/build behavior, not production service integration or bootloader setup.
