# ADR-0647: x86_64 UEFI rescue image architecture

- **Status:** Proposed for maintainer review
- **Issue:** [#647, Decide boot and rescue architecture for the UEFI image](https://github.com/jhuntwork/merelinux/issues/647)
- **Parent:** [#646, Build a UEFI installer and rescue USB image](https://github.com/jhuntwork/merelinux/issues/646)
- **Decision scope:** The first UEFI rescue-boot milestone only. Installer UX, destructive installation, networking, account setup, legacy BIOS, and Secure Boot implementation remain out of scope.

This ADR records one coupled decision. The bootloader, partition table, root format, kernel command line, runtime mounts, and rescue safety rules are one design, not independent options.

## Context

The following are repository or issue facts, rather than new decisions:

- #646 requires an x86_64 UEFI USB environment that can act as an online installer and offline rescue disk. Its first milestone requires a reproducible image, actual firmware-to-bootloader boot in QEMU without `-kernel`, a dinit rescue shell, and recorded inputs and results.
- #647 explicitly defers Secure Boot unless a spike demonstrates a concrete need and requires one coupled decision record.
- #648 will build the image and must pin its source, packages, metadata, signing information, kernel configuration, bootloader, OVMF, build tools, filesystem identifiers, timestamps, and other nondeterministic inputs.
- #649 must use pinned OVMF with a fresh writable NVRAM copy, attach the image as removable media, avoid direct kernel loading, and prove firmware, bootloader, kernel, and dinit startup.
- #650 must use a reproducible system-disk fixture, keep the default read-only rescue path byte-identical, include a dirty-journal fixture, and exercise the selected installed-system entry mechanism offline.
- #634 has local x86_64 evidence for dinit, ext4, mdevd, recovery, serial login, and shutdown/reboot, but its tests directly loaded the kernel and therefore do not prove a bootloader path. Its agreed boot contract has no initramfs and requires dinit to remain PID 1.
- #633 establishes the distro direction: dinit is the init/service manager, s6 support is retired, and the legacy pacman/extlinux/image scripts are historical references only.
- The repository already contains x86_64 recipes for [Limine](../../recipes/core/limine/recipe.kdl), [Linux](../../recipes/core/linux/recipe.kdl), [dinit](../../recipes/core/dinit/recipe.kdl), [mdevd](../../recipes/core/mdevd/recipe.kdl), `busybox`, `e2fsprogs`, and `parted`. The existing Linux common fragment already enables several relevant built-in options, including ext4, VFAT, USB storage, xHCI, and EHCI. The final generated kernel configuration still has to be audited by #648.
- The old [`misc-util/disk_image`](../../misc-util/disk_image) and [`misc-util/livecd`](../../misc-util/livecd) scripts use pacman, extlinux, an initramfs, and privileged host loop/mount operations. They are not an implementation baseline for this design.

## Decision

### 1. Supported boot baseline

The first milestone supports **x86_64 UEFI with Secure Boot disabled**. The QEMU acceptance environment is an x86_64 machine with UEFI firmware and a fresh writable NVRAM file. The test must record the OVMF build and the NVRAM-copy provenance.

The image does not require an existing UEFI boot variable. It is a removable-media image and must boot using the UEFI removable-media fallback path. The test starts with a fresh NVRAM copy and must not rely on `efibootmgr`, a pre-created `Boot####` entry, or a host-specific firmware variable.

Secure Boot signing, key enrollment, shim, and signed-kernel policy are deferred. A later Secure Boot design may add signing inputs, but it must not silently change this milestone's unsigned baseline.

### 2. Removable-media path and bootloader

Use **Limine's x86_64 UEFI loader**, matching the existing `limine` recipe. The image builder must install the Limine EFI executable at exactly:

```text
/EFI/BOOT/BOOTX64.EFI
```

This is the UEFI-defined fallback filename for x86_64 removable media. The builder must verify that the selected Limine release actually produced the x86_64 UEFI executable and must record its source archive hash and resulting EFI binary hash.

The boot configuration and live kernel are also placed on the ESP:

```text
/EFI/BOOT/limine.conf
/EFI/BOOT/vmlinuz
```

This is an intentional Limine layout. Limine's UEFI configuration lookup checks `<EFI app path>/limine.conf` before scanning other partitions, so placing the configuration beside the fallback executable avoids an accidental configuration from the root partition. The current Limine source documents `/EFI/BOOT/limine.conf` as a UEFI-specific lookup path, and the repository's `limine` recipe installs the x86_64 artifact under `usr/share/limine/BOOTX64.EFI`; #648 must copy that artifact to the exact removable-media path above.

The pinned configuration must have the equivalent of:

```text
timeout: 0
graphics: no
serial: yes
interface_branding: MERE-LINUX-UEFI-LIMINE
/Mere Linux Rescue
    protocol: linux
    path: boot:///EFI/BOOT/vmlinuz
    cmdline: root=PARTUUID=<fixed-root-partition-guid> rootfstype=ext4 rootflags=ro,noload rootwait init=/sbin/dinit console=tty0 console=ttyS0,115200n8 loglevel=4
```

`path` is Limine's Linux-protocol kernel path; `kernel_path` is an equivalent alias. The entry has no `module_path`, which is Limine's module/initramfs mechanism. `graphics: no` and `serial: yes` make the QEMU serial transcript include the Limine text menu and branding before Linux starts. The selected Limine release's parser and serial behavior must be checked during the image spike, but changing those options to another boot path is not permitted without a new architecture decision.

Keeping the loader, configuration, and kernel on the FAT ESP avoids making the pre-kernel loader depend on an ext4 implementation or on a second firmware-visible volume. The live root is the GPT root partition loaded by Linux after the kernel starts.

The boot acceptance must capture the `MERE-LINUX-UEFI-LIMINE` branding/menu evidence before the kernel's dinit marker. A kernel-only marker is insufficient evidence of this path.

### 3. Image partition and filesystem layout

The reference image is a **2 GiB GPT raw disk image** suitable for writing directly to removable media. The size is a versioned build input; the builder fails rather than silently changing it if the pinned package set no longer fits.

| GPT item | Size/layout | Filesystem and role |
| --- | --- | --- |
| ESP | First partition, 256 MiB | FAT32. Contains `EFI/BOOT/BOOTX64.EFI`, `limine.conf`, and `vmlinuz`. |
| root | Second partition, remainder of the image | ext4. Contains the dinit rescue userspace, tools, service graph, and static configuration. |
| persistence | None | The first milestone has no writable persistence partition. |

The partition type GUIDs, disk GUID, ESP partition GUID, root partition GUID, FAT volume ID, ext4 filesystem UUID, filesystem feature choices, and fixed image size are explicit manifest inputs. They are selected once for a build line and reused for its reproducibility comparison. They must never come from the clock or a random UUID call during a build.

The live root partition is mounted read-only by the kernel. Runtime writes go to tmpfs mounts described below. This protects the rescue medium from routine service writes and makes the live environment's persistence behavior clear: changes made in a rescue session are intentionally discarded at shutdown.

The separate installed-system fixture is not this image. Its initial supported layout is also GPT with a 256 MiB FAT32 ESP and an ext4 root partition, with the installed kernel under `/boot/vmlinux` and the root filesystem identified by UUID/PARTUUID in its fstab and boot configuration. It has no swap partition in the first fixture. This is the layout assumed by the offline rescue test and is the migration/layout contract called out in the #633 section below.

### 4. Live root, discovery, timing, and command line

The live root is a normal ext4 filesystem, not a squashfs image, an ISO9660 filesystem, or a filesystem hidden behind an overlay. Linux discovers it directly from its GPT partition GUID. The command line supplied by Limine is semantically:

```text
root=PARTUUID=<fixed-root-partition-guid> \
rootfstype=ext4 rootflags=ro,noload rootwait \
init=/sbin/dinit \
console=tty0 console=ttyS0,115200n8 loglevel=4
```

The generated Limine configuration may use the pinned release's exact syntax for the kernel path, but it must preserve those values. It must not include `initrd=` or an equivalent module. `rootwait` is required because USB enumeration can complete after firmware transfers control to the kernel. The root device must not be selected by `/dev/sdX`, which is unstable across enumeration order.

The required timing contract is:

1. UEFI locates `/EFI/BOOT/BOOTX64.EFI` without a firmware variable.
2. Limine loads the kernel and passes the fixed root PARTUUID and `rootwait`.
3. Built-in USB, block, partition, and ext4 support allows the kernel to wait for the removable root device and mount it read-only.
4. The kernel starts `/sbin/dinit` as PID 1.
5. The dinit live service graph mounts only virtual filesystems, starts mdevd, performs coldplug, starts the configured console service, and prints the deterministic rescue-ready marker.

#### No-initramfs interpretation

For this project, **an initramfs means any filesystem archive or equivalent early userspace supplied to the kernel or bootloader before the root filesystem**. An embedded kernel initramfs (`CONFIG_INITRAMFS_SOURCE`, an appended cpio archive, or an `initrd`/`initramfs` Limine entry) therefore violates the no-initramfs decision just as an external initrd does.

The kernel may contain built-in drivers and built-in kernel data required to reach the root device. Those are not an initramfs. The build must set `CONFIG_INITRAMFS_SOURCE` empty and must show that no initramfs is present in the image or Limine configuration.

### 5. Built-in kernel capabilities

The final x86_64 kernel configuration must audit and prove the following are built in (`=y`), not modules. The list names the capabilities needed by this image; #648 must record the final option names and the generated `.config` because Linux version changes can split or rename dependencies.

- UEFI handoff and early console support: EFI support, EFI stub support where required by the selected kernel build, VT, framebuffer/simple framebuffer, and the 8250 serial console used by QEMU.
- GPT partition discovery: EFI/GPT partition support and the block-device core.
- USB removable storage: USB core, the controller used by the acceptance VM (xHCI, with EHCI retained for the baseline compatibility path), USB mass storage, SCSI disk support, and the SD/block dependencies selected by the final QEMU attachment method.
- Root filesystem: ext4 and its block/compression dependencies.
- ESP inspection: FAT and VFAT plus the required NLS tables. Linux does not need to mount the ESP to boot, but the rescue tool set must be able to inspect it.
- Virtual boot filesystems: devtmpfs, procfs, sysfs, tmpfs, devpts, and shared-memory support. `DEVTMPFS_MOUNT` is not a substitute for the dinit service graph; the graph must make the mount policy visible.

The current `mere-common.config.fragment` already sets `CONFIG_EXT4_FS=y`, `CONFIG_VFAT_FS=y`, `CONFIG_USB_STORAGE=y`, `CONFIG_USB_XHCI_HCD=y`, and `CONFIG_USB_EHCI_HCD=y`, among other options. That repository fact is useful starting evidence, not acceptance by itself. #648 must confirm the transitive SCSI, GPT, USB, console, and root dependencies are built in and must add a dedicated image fragment if the general kernel fragment is insufficient.

### 6. Writable runtime state

The live root remains read-only. The dinit live profile creates these volatile mounts before starting services that need them:

```text
/dev       devtmpfs
/proc      proc
/sys       sysfs
/dev/pts   devpts
/dev/shm   tmpfs
/run       tmpfs
/tmp       tmpfs
/var/log   tmpfs
/var/tmp   tmpfs
```

The service graph creates required directories and permissions in those tmpfs filesystems. `/run/dinitctl`, mdevd state, service logs, shell history, temporary downloads, and other runtime state therefore never write to an attached Mere system disk. The live image's root itself is also protected by `ro,noload`.

The dinit live profile must not include a generic `mount-rw` action that remounts the live root. The existing #634 boot graph can be reused only after it has a read-only-root variant with tmpfs runtime mounts and the same mdevd readiness/coldplug ordering.

### 7. Disk-safety contract

The default rescue boot and the default inspection sequence obey all of these rules:

- The only automatic disk mount is the live USB root needed to boot. Attached Mere system disks are never automounted.
- No attached system-disk swap is activated. The live image has no swap entry or automatic swap service.
- No attached system-disk filesystem is opened writable by boot or discovery.
- No `fsck`, repair tool, journal replay, package transaction, generation activation, or bootloader installation runs automatically.
- Device discovery may enumerate block devices and read partition/filesystem metadata, but it must not call a mount helper as a discovery side effect.
- The supported read-only ext4 mount uses `ro,noload`, which prevents ext4 journal replay. A dirty-journal fixture must demonstrate that this option is present and that the fixture hash is unchanged.
- A writable mount, filesystem repair, swap activation, or other mutation requires a deliberate operator command after the target has been identified. Those actions are separate tests against a disposable fixture and are not part of the first milestone's default path.

A rescue UI or helper may make these actions easier later, but it must retain the same explicit-action boundary. The first milestone can use documented shell commands rather than committing to installer UX.

### 8. Rescue tools and installed-system entry

The minimum offline tool surface is:

- block and filesystem discovery by stable identifiers (`lsblk`, `blkid`, or equivalent),
- partition inspection (`parted` or equivalent),
- ext4 inspection and check tooling (`e2fsck`, `tune2fs`, and/or `debugfs` as packaged),
- explicit `mount` and `umount`,
- a POSIX shell, core file utilities, `dinitctl`, and serial/tty access,
- the documented installed-system entry helper or command sequence.

The image package set must contain providers for those capabilities, plus `linux`, `dinit`, `mdevd`, and the pinned Limine boot files. The current recipe tree proves some providers (`busybox`, `e2fsprogs`, `parted`, `dinit`, `mdevd`, and `linux`) but does not prove that all discovery commands are already packaged in the new recipe format. #648 must map each required command to a package and add only the narrowly needed recipe/package work. XFS, Btrfs, LVM, encryption, and network-dependent recovery are not first-milestone supported filesystems or workflows.

“Enter the installed system” means a deliberate, offline chroot into the selected supported root, initially mounted read-only. The documented sequence is equivalent to:

```text
mount -o ro,noload <installed-root> /mnt/mere
mount --rbind /dev /mnt/mere/dev
mount --make-rslave /mnt/mere/dev
mount -t proc proc /mnt/mere/proc
mount --rbind /sys /mnt/mere/sys
mount --make-rslave /mnt/mere/sys
mount --rbind /run /mnt/mere/run
mount --make-rslave /mnt/mere/run
chroot /mnt/mere /bin/sh
```

The helper must verify that `/mnt/mere` is the explicitly selected target and must provide cleanup commands that unmount in reverse order. These mounts are namespace/runtime mounts and do not modify the target disk. The target remains read-only during the default entry sequence. A later operator may deliberately remount it writable for repair; that is outside the default acceptance path. The entry sequence does not start the installed dinit instance or require networking.

### 9. Reproducibility bar and pinned inputs

The reproducibility bar is **byte identity of the complete raw image** for two clean builds from the same manifest and source inputs. Component hashes are additional evidence, not a reason to accept differing bytes. If a tool emits nondeterministic bytes, #648 must normalize the input or fail the build rather than downgrade this bar silently.

The machine-readable build manifest must include, with immutable versions and hashes where applicable:

- the Merelinux source revision and image-builder revision;
- the exact Mere binary/revision used by the build, package repository snapshot or metadata revision, package versions, package archive hashes, and the public repository signing key;
- the exact kernel source archive, generated kernel configuration, configuration fragments, compiler/toolchain and container image digests;
- the Limine source release/archive hash, build configuration, EFI output hash, and configuration file;
- the OVMF source/build and firmware-code hash used by #649, plus the fresh NVRAM template/copy provenance;
- all image-builder tools and versions, including GPT, FAT, ext4, archive, hashing, and QEMU tools;
- fixed disk size, GPT GUIDs, partition GUIDs, filesystem UUIDs, FAT volume ID, ext4 feature set, file ownership/modes, `SOURCE_DATE_EPOCH`, timezone, locale, umask, and any compression settings;
- the exact commands and environment assumptions used to build the image and fixture; and
- BLAKE3 (and any tool-required secondary) digests for the complete image, ESP contents, root contents, and fixture.

The build must occur in a clean environment with no undeclared host package or host `/dev` dependency. The output manifest itself is evidence and must be reproducible or separately excluded from the image with its own digest.

### 10. Reproducible system-disk fixture

Issue #648 produces a separate raw fixture for #650. It uses the installed-system layout in section 3 and a deterministic root tree containing:

- a minimal dinit-based installed system with `/boot/vmlinux`, `/etc/fstab`, hostname, and recognizable files;
- the exact Mere package/layout revision and package metadata selected for the fixture;
- a FAT32 ESP with fixed contents and IDs; and
- an ext4 root with fixed UUID, feature flags, ownership, modes, timestamps, and file order.

The fixture builder records its source tree, package inputs, commands, IDs, and complete-image digest. It creates a second **dirty-journal variant** by making a known file change and capturing the disk before a clean unmount. #650 uses that variant to prove the default `ro,noload` sequence does not replay the journal or change any block.

The fixture is disposable. Read-only discovery, `ro,noload` mounting, and the chroot entry path compare whole-disk hashes before and after. Any difference fails acceptance.

### Required dependency handoff, without blocking on closure

### Deliverables required from #634

Issue #634 does not need to close before the image work starts, but the image pipeline and QEMU test require these concrete outputs:

1. A packaged dinit executable and `dinitctl` with the selected version and package hash recorded.
2. A dinit service profile for the live image: virtual filesystem setup, read-only root handling, mdevd readiness followed by coldplug, console access, the deterministic rescue-ready marker, and orderly shutdown without an automatic reboot loop.
3. The read-only-root/tmpfs runtime variant described in this record. The existing test profile's writable-root assumption cannot be copied unchanged.
4. The recovery behavior and failure semantics already demonstrated in #634: preserve diagnostics and make foundational failures recoverable through dinit's console path rather than silently rebooting.
5. The serial console/getty configuration needed by QEMU. A tty1 login remains the default contract; the QEMU profile enables the serial getty as an explicit machine option.

The broader #634 guest matrix, essential-service validation, and s6 removal are not prerequisites for this first image milestone.

### Assumptions required from #633

The first rescue implementation assumes the migration direction already stated in #633:

- dinit is the installed system's PID 1 and service manager; s6 service directories are not required by the fixture or rescue profile;
- installed systems boot locally through UEFI with a GPT ESP and an ext4 root, without an initramfs;
- the installed kernel is available under `/boot/vmlinux`, and root identity is represented by stable UUID/PARTUUID values rather than `/dev/sdX`; and
- the rescue entry path treats package generations and service state as installed-system data to inspect, not as a reason to activate a generation or start services.

If #633 changes the final installed layout, it must publish a compatibility mapping before #650 runs. That is a migration input, not a requirement that the broader issue be closed.

## Consequences

This decision produces a small, directly writable GPT rescue image that can prove the complete UEFI-to-Limine-to-kernel-to-dinit path without firmware-variable setup or an initramfs. It reuses the repository's existing Limine, Linux, dinit, and mdevd direction and keeps the live root and tested system-disk fixture on the same ext4/dinit model.

The design also imposes deliberate limits and costs:

- The first milestone supports only x86_64 UEFI, Secure Boot disabled, ext4, and the defined GPT layouts. Legacy BIOS, other architectures, other root filesystems, and Secure Boot need separate decisions.
- The live image has no persistence partition. Runtime state is volatile and a rescue session cannot retain changes unless an operator deliberately writes to a selected disk.
- Built-in USB, GPT, filesystem, and console support increases the kernel image and requires a generated-configuration audit rather than relying on modules.
- The dinit service graph needs a read-only-root/tmpfs profile distinct from the existing writable-root test profile.
- Fixed identifiers and timestamps improve reproducibility but become part of the image format contract. Changing them requires a new image-input revision and updated fixtures.
- Disk safety moves mutation decisions into explicit operator actions. That is safer for recovery, but it means automatic discovery cannot also provide automatic mounting or repair.
- Limine's serial-visible branding and the pinned OVMF/QEMU setup become acceptance dependencies. A mere kernel or dinit marker cannot substitute for bootloader evidence.

## Rejected alternatives

- **GRUB or systemd-boot:** Both can boot UEFI media, but neither is selected for this milestone. Limine is already an x86_64 UEFI recipe in this repository and gives one small removable-media fallback executable without adding GRUB modules or a systemd-boot policy. A later bootloader comparison can replace it only with a new coupled decision.
- **extlinux and syslinux:** These are explicitly rejected, not fallback choices. The old scripts use extlinux/syslinux and an MBR path, while this milestone requires Limine's UEFI executable at `/EFI/BOOT/BOOTX64.EFI`. They cannot satisfy the selected UEFI removable-media contract and would reintroduce the historical BIOS-oriented path that #646 defers.
- **A Limine BIOS or hybrid-BIOS image:** Limine is selected, but only its x86_64 UEFI executable and UEFI fallback path are in scope. No `limine-bios.sys`, BIOS stage, MBR installation, or hybrid BIOS/UEFI artifact is part of this milestone.
- **A firmware-installed boot entry:** It is unsuitable for a USB rescue image because it makes the image depend on host NVRAM. `/EFI/BOOT/BOOTX64.EFI` is the portable fallback contract.
- **ISO9660 or a hybrid ISO as the primary artifact:** It weakens the explicit GPT/ESP/root contract and makes the raw removable-disk layout and separate system-disk fixture less direct. The first artifact is a GPT raw image.
- **FAT32 as the live root:** FAT does not provide the Unix permissions, device semantics, symlinks, and service layout required by a dinit root.
- **Squashfs plus overlay or a compressed root plus initramfs:** This would require an early userspace and complicate root discovery and writable-state accounting. It is rejected by the no-initramfs interpretation and by the need to keep the first design close to the proven ext4/dinit path.
- **A writable ext4 live root or a persistence partition:** Both make routine state writes easy to confuse with intentional target-disk actions and make the default state less clear. tmpfs runtime state gives the rescue shell what it needs without persistence.
- **Automatic filesystem probing/mounting, swap activation, fsck, or journal replay:** These violate the explicit #647/#650 disk-safety contract. Discovery and mutation are separate operator actions.
- **Root selection by `/dev/sdX` or “first removable disk”:** USB enumeration order is not stable and could select the attached system disk. The live root uses a fixed PARTUUID; rescue selection requires explicit operator identification.
- **Direct QEMU `-kernel` loading:** It was useful in #634's dinit tests but cannot prove UEFI firmware or the image bootloader and is explicitly prohibited by #646 and #649.

## Implementation handoff

### Exact first-milestone acceptance criteria

The first milestone is complete only when every item below passes and its evidence is recorded in the #646 milestone notes:

1. **Clean reproducible build:** From the documented clean environment, pinned manifest, and pinned inputs, #648 produces one 2 GiB GPT raw image and one system-disk fixture without undeclared host dependencies. The manifest records inputs, commands, assumptions, IDs, and output digests.
2. **Reproducibility:** Two clean builds from identical pinned inputs produce byte-identical complete rescue images. The comparison covers GPT headers, partition tables, ESP, root filesystem, file metadata, and unused image space, not just extracted files. The fixture has the same reproducibility evidence.
3. **Correct removable layout:** The image has a GPT with the 256 MiB FAT32 ESP and ext4 root. The ESP contains `/EFI/BOOT/BOOTX64.EFI`, the pinned Limine configuration, and the pinned x86_64 kernel. No firmware variable or pre-existing NVRAM entry is needed.
4. **Actual UEFI boot:** With pinned OVMF, a fresh writable NVRAM copy, the image attached as the intended removable USB device, and networking disabled, QEMU boots through firmware and Limine. The command uses neither `-kernel` nor another direct kernel-loading shortcut. The log contains bootloader-path evidence, the kernel console, the dinit PID 1 marker, and the deterministic rescue-ready marker.
5. **Working rescue shell:** The boot reaches an authenticated/usable dinit rescue shell on the serial console. The shell can run the minimum discovery, partition, ext4 inspection, explicit mount, and unmount commands. The log records the exact QEMU command, firmware hashes/provenance, image digest, and observed output.
6. **No initramfs:** The Limine entry has no `initrd`/`initramfs`; the image has no embedded or external early-userspace archive; `CONFIG_INITRAMFS_SOURCE` is empty; and the root is reached by built-in kernel drivers plus `root=PARTUUID` and `rootwait`.
7. **Safe default state:** Boot does not automount an attached Mere system disk, activate its swap, run repair, replay its journal, or open it writable. Runtime state is on the defined tmpfs mounts. The acceptance record states the supported x86_64, ext4, UEFI, Secure-Boot-disabled limits.
8. **Dependency traceability:** The result names the exact #634 dinit package/service/console deliverables and the #633 migration/layout assumptions used. Neither issue's broad closure is a prerequisite.

These criteria deliberately stop before installer UX, networking, destructive installation, account setup, Secure Boot, legacy BIOS, and installed-system boot without the USB image. Those are later #646 phases.

### Swamp/Mere workflow handoff

The installed workflow documentation separates recipe development from Mere source development and from shell execution. That separation matters to the later issues:

- For a recipe/package input used by #648, `@jeremy/mere-dev` invokes `mere dev validate`, `mere dev build`, `mere dev hash`, and import operations directly. It owns a dedicated Mere root; it must not be wrapped in `@jeremy/mere-shell`, because that would create nested namespaces.
- For an installed-profile smoke command, `@jeremy/mere-shell` requires an explicit package list and exact `argv` array. If #648 uses it for a package smoke check, it must pin the same Mere version and shared dedicated root as the corresponding `mere-dev` operation and record both in the manifest. Shell command strings are not an acceptable substitute for exact argv.
- `@jeremy/mere-pm-dev` and its `mere-change-prepare`/`mere-change` workflows validate and deliver changes to the Mere package-manager source tree with fixed Zig commands. They are not image builders, recipe builders, or rescue QEMU harnesses. The `@jeremy/merelinux-change` workflow is the recipe-change delivery path and is likewise not a substitute for the dedicated image pipeline or UEFI acceptance harness.
- #649 and #650 are host-side, offline QEMU/fixture acceptance work. They must invoke the pinned QEMU and OVMF artifacts from the #648 manifest and must not turn a Mere shell namespace into evidence of firmware boot.

These are execution constraints for the follow-on work, not additional architecture decisions.

### Implementation notes and remaining validation

No architectural decision is left open. The following are implementation validations for #648–#650, not alternate designs:

- Confirm the exact Limine configuration syntax and the pinned release's serial-visible bootloader output. The required paths and options are shown in section 2. If the release cannot provide the required evidence, stop for review rather than substituting extlinux, syslinux, or another bootloader.
- Audit the generated Linux `.config` for every built-in dependency listed above, including the final QEMU USB controller and GPT parser.
- Map each rescue command to an actual package recipe and record the provider in the image manifest. Do not infer that a library recipe provides command-line tools.
- Verify the dinit read-only-root live profile, failure behavior, and serial marker using the #634 package versions selected for the image.
- Verify `ro,noload` and whole-disk hash preservation against both clean and dirty-journal ext4 fixtures.
