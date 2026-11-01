# Mere boot services

`mere-boot` supplies the minimum local-disk boot graph for dinit. Networking,
SSH, time synchronization, D-Bus, and desktop services are optional. No
initramfs is required; the kernel must contain the root-disk/filesystem drivers,
console support, and automatic devtmpfs mounting needed to reach `/sbin/init`.

## Installation contract

Install `busybox`, `dinit` (unpatched 0.22.1 is sufficient), `mdevd` (release 2 or later),
`shadow`, and `mere-boot` into the **system** profile with
`settings { init-provider "dinit"; }` in Mere's
configuration. These are explicit installation requirements: recipe `depends`
lists build inputs, and script-invoked programs are not inferred ELF dependencies.
The image or installer must expose the active system generation's `bin`, `sbin`,
`lib`, and `usr` directories at the filesystem root. Boot the kernel with
`init=/sbin/init`; the launcher execs dinit so it remains PID 1.

Provision the root directories `/dev`, `/proc`, `/sys`, `/run`, `/tmp`, `/var`,
`/root`, and `/home` before booting a read-only root. `/usr` and the Mere store
must be accessible on the root filesystem before init starts. A separately
mounted early `/usr`, encrypted root, and remote root need additional design.
Provide an `/etc/fstab` containing the required local mounts (an empty file is
valid), account databases, a usable Shadow/PAM login configuration, and an
administrator-provisioned root credential. This package never sets a password,
unlocks an account, or creates an unauthenticated recovery shell. Its minimal
`/etc/profile` default makes both `/bin` and `/usr/bin` (and administrative paths)
available in a login shell; an existing administrator profile is preserved.

Mere generates the ordinary service descriptions in `/usr/share/dinit.d` during
system-profile activation. The `boot`, `recovery`, and `single` descriptions are
package `/etc` defaults because bundles and console attachment are not currently
expressible with service primitives. They are copied by normal activation when
absent; existing administrator files remain unchanged. Review `mere etc diff`
and merge relevant defaults on an existing installation. Do not replace the
whole machine's `/etc` merely to adopt this package.

## Graph and ordering

- `mount-proc` establishes procfs. `mount-sys`, `mount-dev`, and `mount-rw` depend
  on it and establish sysfs, devtmpfs, and a writable root.
- `mount-runtime` waits for those services, establishes `/run`, devpts and shared
  memory, sets the temporary-directory mode, and exposes `/dev/fd`.
- mdevd starts after those mounts and signals readiness. Its coldplug service
  creates the libudev-zero runtime directory and then enumerates devices.
- `mount-fstab` waits for coldplug before mounting the local filesystems.
- `system-setup` creates log/home directories, applies optional hostname and
  sysctl configuration, and enables configured swap. `sysinit` requires it.
- `tty1` waits for `sysinit` and starts BusyBox getty with Shadow login. The
  default `boot` bundle requires both `sysinit` and `tty1`.

The init launcher prepares `/run` before dinit creates its control socket, so a
later tmpfs mount cannot hide `/run/dinitctl`. The graph's runtime-mount helper
recognizes this existing mount. Setup is otherwise performed by recipe service
primitives, whose helpers use POSIX shell and BusyBox utilities.

The startup mount services deliberately do not unmount filesystems when released:
a partial boot may need those filesystems for authenticated recovery. On normal
shutdown dinit stops the complete service set first; its shutdown utility then
terminates remaining processes, disables swap, syncs, and unmounts/remounts
filesystems before invoking kernel power-off or reboot. Do not add early mount
stop commands which race optional daemons during shutdown.

## Machine configuration and failure handling

`/etc/dinit.d/boot.d` is the administrator's optional-service set. For a QEMU or
headless machine with a `ttyS0` serial console, enable the supplied serial service:

```sh
mkdir -p /etc/dinit.d/boot.d
ln -s /usr/share/dinit.d/ttyS0 /etc/dinit.d/boot.d/ttyS0
```

This records next-boot intent; use `mere start ttyS0` separately to start it now.
The supplied serial speed is 115200. Other ports/speeds can use an administrator
service override. Optional-service failures do not satisfy or replace the
required foundational graph. Optional daemons with additional filesystem/device
requirements should declare those dependencies in their own recipes.

Setup diagnostics go to the kernel-selected console; dinit also writes
`/run/dinit.log`, including failures before `/var` is mounted. Daemons using
Mere's ordinary logging metadata retain their own configured log files. Log
rotation is separate work.

A required setup failure prevents normal boot completion. Dinit presents its
boot-failure menu on the console; select `e` for recovery. Recovery then starts
a console-attached Shadow login, initially requesting root. Automatic recovery
is left disabled so the menu and login never compete for console input.

The helper reopens dinit's control socket after failed startup so lifecycle and
shutdown commands remain available. Credentials and normal PAM policy still
apply; locked or missing credentials do not grant a shell. There is no automatic
reboot. Recovery does not depend on `sysinit`, so failure of that graph cannot
suppress the recovery login. An operator repairs the system and explicitly
requests reboot or power-off. `single` selects the same authenticated recovery
path directly.
