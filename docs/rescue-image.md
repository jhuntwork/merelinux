# Rescue image build pipeline

`misc-util/rescue-image-build` is the #648 host-side assembler. It consumes
staged Mere package trees, a staged x86_64 kernel, and the Limine EFI output. It
produces a 2 GiB GPT raw rescue image, a separate installed-system fixture, a
dirty-journal fixture, and `manifest.json`.

The assembler is deliberately fail-closed. It requires the fixed inputs in
`misc-util/rescue-image.inputs.json`, root for loop/mount operations, the pinned
image tools, and two clean-build comparisons. A single build cannot be reported
as reproducible.

The selected Mere version is `0.23.0` throughout the image-tool profile and
binary input. The pinned x86_64 Mere binary SHA-256 is
`3250c04b7f288056f5db8860a644a17895a7dc6398ddc961e1316bfe928ea631`.
The rescue package set is rolling: the profile names packages without versions,
and `mere profile apply` refreshes the configured repository before resolving
the latest x86_64 artifacts. The realized profile records the versions and
content hashes used for that build, but those values are observations rather
than package-selection pins.
The same pinned binary is copied into the final rescue root at `/usr/bin/mere`.
The final root preserves the Mere store at `/mere/store` and the active system
projection at `/mere/profiles/system/current`; root-level package files remain
symlinks into that store so the installed packages are inspectable and Mere can
operate on them after boot. The rescue root also contains the `curl` command,
its shared runtime libraries, and the pinned CA bundle. The image configures
loopback and `eth0` for DHCP in `/etc/network/interfaces`. The `network-dhcp`
dinit service scans non-loopback interfaces and runs BusyBox `udhcpc` on the
first one that accepts a lease, which also writes `/etc/resolv.conf` from the
DHCP-provided DNS servers.
The assembler uses `parted` to inspect the deterministic GPT after
writing fixed GUIDs, and uses `mere dev hash` for BLAKE3 digests. It does not
require `sgdisk` or a separate `blake3` executable.

## Package preparation

Use the existing Swamp workspace at `/home/jeremy/swamp-workspace` as
`SWAMP_REPO`. Create dedicated behavior definitions with separate roots. Do not
reuse an unrelated shell root, and do not run `mere-dev` inside `mere-shell`:

```sh
export SWAMP_REPO=/home/jeremy/swamp-workspace
swamp behavior create @jeremy/mere-dev mere-rescue-dev-023 \
  --repo-dir "$SWAMP_REPO" \
  --global-arg mereVersion=0.23.0 \
  --global-arg mereRoot="$PWD/.swamp/mere-rescue-dev-023/root"
swamp behavior create @jeremy/mere-shell mere-rescue-shell-023 \
  --repo-dir "$SWAMP_REPO" \
  --global-arg mereVersion=0.23.0 \
  --global-arg mereRoot="$PWD/.swamp/mere-rescue-dev-023/root"
swamp behavior create @jeremy/mere-shell mere-rescue-tools-023-hoststore \
  --repo-dir "$SWAMP_REPO" \
  --global-arg mereVersion=0.23.0 \
  --global-arg mereRoot=/ \
  --global-arg useHostStore=true
```

The assembler initializes each isolated Mere root from the official repository
files before syncing: `https://pkgs.merelinux.org/config.kdl` and
`https://pkgs.merelinux.org/mere.pub`. It adds the required dinit provider
setting to that downloaded config, copies both files into the final image under
`/mere`, and records their SHA-256 values in the manifest. The root therefore
has the trust material needed for `mere` commands after boot, not only the
realized package files.

Build the non-kernel tool-profile recipes only when provisioning the separate
image-tool profile. The rescue package set is not compiled here; it is resolved
from the configured rolling Mere repository by `profile apply`:

```sh
cat > rescue-profile.kdl <<'EOF'
profile {
  package "busybox"
  package "curl"
  package "dinit"
  package "e2fsprogs"
  package "linux"
  package "limine"
  package "mdevd"
  package "mere-boot"
  package "parted"
  package "shadow"
}
EOF
mere --root "$MERE_ROOT" sync
mere --root "$MERE_ROOT" profile apply rescue-profile.kdl
```

The isolated Mere root is configured with `init-provider "dinit"` and the
profile is applied to its system profile. System-profile activation generates
Mere's package-owned dinit service files under `/usr/share/dinit.d`; applying a
named profile would omit that service graph. The assembler materializes the
active system generation, preserves its store and profile projection in the
image, applies `etc-defaults` to `/etc`, and adds the rescue-specific DHCP and
readiness services under `/etc/dinit.d`. The normal
`mere-boot` serial getty remains the console entry point. The assembled USB
provisions the root account with the shared operator password `rescue` so that
the console is usable after the operator selects the root login. The login name
is `root`, and the shared password is `rescue`. This credential is convenience
for physical rescue media, not a protection boundary; anyone who can modify or
boot the USB can replace it. Do not reuse it for network services.

The pinned tool profile uses `busybox`, `parted`, and `e2fsprogs`. Busybox
supplies the `mkfs.vfat` and `losetup` applets. E2fsprogs supplies `mkfs.ext4`,
`tune2fs`, and `debugfs`. The configured Mere repository does not currently
provide `dosfstools` or `util-linux`, so those package names are not claimed.

Run the profile smoke with an explicit package list and exact argv:

```sh
misc-util/rescue-image-build --tool-profile-smoke \
  --tool-shell-behavior mere-rescue-tools-023-hoststore \
  --swamp-repo-dir "$SWAMP_REPO"
```

The `useHostStore=true` binding must use `mereRoot=/` (an empty
`mereRoot` is also accepted by `@jeremy/mere-shell` 2026.11.04.2). This is
different from the isolated `mere-rescue-tools-023` binding, which keeps its
own dedicated root for recipe and development work. The published extension
maps `/` to the host Mere tree and exposes its existing `/mere/store`; it does
not create the legacy self-referential store symlink. The host Mere store must
already be initialized and readable by the execution worker.

The smoke runner checks each returned resource's `success`, `exitCode`, and
reported Mere version. `tune2fs -V` prints its version but exits with status 1
in the pinned e2fsprogs package, so that one command records
`expected_exit_code: 1` rather than pretending that a nonzero result succeeded.
A Swamp wrapper can report `status: succeeded` while this resource still has
`success: false`; inspect the resource fields before treating smoke as valid.
On this host, the current Swamp worker is rootless and cannot mount the host
Mere tree for namespace execution, so the published binding reaches Mere 0.23.0
but the namespace launcher returns `/bin/sh` not found. The profile itself is
valid: Mere's profile is a symlink-tree projection under
`<root>/mere/profiles/<name>/root`, and its package links intentionally target
logical `/mere/store/...`. With host root `/`, those links resolve through the
host Mere store. This is an execution-environment blocker, not evidence that a
guessed store path or shell wrapper is safe. The direct privileged Mere check
remains separate evidence for package contents.

### Direct named profile validation

For host-side validation, create and apply the named profile with the pinned
Mere 0.23 binary in a mount-capable environment:

```sh
mere --root / profile create mere-rescue-tools-023-hoststore
mere --root / profile apply "$PWD/.swamp/mere-shell/profiles/profile.kdl" \
  --profile mere-rescue-tools-023-hoststore
mere --root / profile packages --profile mere-rescue-tools-023-hoststore
```

Mere records the active profile root at
`/mere/profiles/mere-rescue-tools-023-hoststore/root`. Set
`TOOL_PROFILE_ROOT` to that recorded root and invoke the required binaries by
their profile-root paths when testing the host-side boundary, for example
`$TOOL_PROFILE_ROOT/sbin/parted`, `$TOOL_PROFILE_ROOT/sbin/mkfs.vfat`,
`$TOOL_PROFILE_ROOT/sbin/mkfs.ext4`, `$TOOL_PROFILE_ROOT/sbin/losetup`,
`$TOOL_PROFILE_ROOT/sbin/tune2fs`, and `$TOOL_PROFILE_ROOT/sbin/debugfs`.
This uses the published symlink-tree contract directly, without a shell wrapper
or guessed store path. Loop setup and mount operations still run as explicit
host operations under root.

The assembler receives `--tool-profile-root` explicitly and fails closed if
the root lacks `profile.kdl`, `realization.v1`, the pinned package names, or any
required profile executable. The assembler records the profile root and the
resolved profile executable paths in `manifest.json`. `mount`, `umount`,
`mere`, and `tar` remain deliberate host-side dependencies; they are not
looked up in the Mere profile.

The top-level `--build --pull-packages` path performs a rolling profile
resolution before assembly. It refreshes repository metadata, applies the
unversioned package names from `rescue-image.inputs.json`, and materializes the
resolved profile into the rescue root. The profile's `/mere/store` and
`/mere/profiles/system/current` projections are retained in the image rather
than flattened into ordinary files, so absolute profile links remain valid
after boot. The package manifest records every resolved dependency's version
and content hash as provenance, plus the requested package names; it does not
constrain the next run to those values.
Mere's `etc-defaults/` package trees are materialized into `/etc` because no
Mere activation runs inside the rescue image. The separate image-tool profile
remains pinned because it supplies the host-side formatters and OVMF build
inputs. The path does not invoke `mere dev build`.
The kernel audit follows the real 6.18.62 configuration symbols; x86_64 also
enables the KVM core and Intel/AMD backends as modules.

OVMF preparation is pinned to Tianocore `edk2-stable202608`, commit
`2970e5699ba6267f3384ffab20f96647578aebc8`, from the codeload source archive
whose SHA-256 is
`bac40812213576c3025cf780c33d882f9e087a44201b1cd28a07f6d1eb54b76a`.
The pipeline verifies that digest before recursive checkout, builds
`OvmfPkg/OvmfPkgX64.dsc` with `CLANGDWARF`, `RELEASE`, `NETWORK_ENABLE=FALSE`,
`SECURE_BOOT_ENABLE=FALSE`, and `SMM_REQUIRE=FALSE`, and copies a fresh
`OVMF_VARS.fd` template with deterministic timestamps. ACPICA `iasl` is built
from the separately pinned ACPICA source archive. The verified codeload
archive is retained and SHA-256 checked as source provenance, but it is not
used as the build tree because it omits required submodules. The pipeline
that commit detached, initializes every submodule recursively (including
submodules marked `update=none`), and verifies every checked-out gitlink before
BaseTools runs. The firmware manifest records the git URL, superproject commit,
archive digest, and every verified submodule commit. It does not silently use
unpinned submodule heads or host firmware.

## Assembly inputs and command

The assembler installs the dinit service profile from
`misc-util/rescue-services` under `/etc/dinit.d/`, and audits `/boot/config`.
The OVMF build uses a dedicated Mere 0.23 profile containing `llvm`, `nasm`,
`flex`, `bison`, `make`, `m4`, and `util-linux-libs-dev`. Its recorded root is
`/mere/profiles/mere-rescue-ovmf-023/root`; the active package versions and
content hashes are written into the firmware manifest. The profile supplies
Clang/Clang++, NASM, Make, Flex, Bison, m4, Python, and the UUID development
headers. ACPICA iasl is built from
the separately pinned ACPICA source archive above.

```sh
misc-util/rescue-image-build --prepare-generated-inputs --pull-packages \
  --mere-dev-root "$MERE_ROOT" \
  --mere-binary "$MERE_BINARY" \
  --mere-version 0.23.0 \
  --tool-profile-root "$TOOL_PROFILE_ROOT" \
  --ovmf-tool-profile-root /mere/profiles/mere-rescue-ovmf-023/root \
  --output-dir out/rescue-image
misc-util/rescue-image-build --build \
  --mere-dev-root "$MERE_ROOT" \
  --mere-binary "$MERE_BINARY" \
  --mere-version 0.23.0 \
  --tool-profile-root "$TOOL_PROFILE_ROOT" \
  --root-tree out/rescue-image/generated-inputs/rescue-root \
  --kernel out/rescue-image/generated-inputs/rescue-root/boot/vmlinux \
  --limine-efi out/rescue-image/generated-inputs/limine.efi \
  --package-manifest out/rescue-image/generated-inputs/package-manifest.json \
  --firmware-manifest out/rescue-image/generated-inputs/firmware-manifest.json \
  --output-dir out/rescue-image
```

The preparation command resolves the eight requested package names from the
configured rolling repository. Mere records all resolved dependencies and
content hashes in the package manifest as build provenance.

A representative package manifest has this shape:

```json
{
  "mere": {
    "version": "0.23.0",
    "binary_blake3": "<mere-binary-hash>",
    "binary_sha256": "3250c04b7f288056f5db8860a644a17895a7dc6398ddc961e1316bfe928ea631",
    "repository_snapshot": "<snapshot>"
  },
  "requested_packages": ["busybox", "curl", "dinit", "e2fsprogs", "linux", "limine", "mdevd", "parted"],
  "packages": [
    {"name": "curl", "version": "<resolved-version>", "content_blake3": "<content-hash>"}
  ],
  "providers": {
    "/bin/curl": "rolling-profile",
    "/boot/vmlinux": "linux",
    "/boot/config": "linux"
  },
  "tool_profile_packages": [
    {"name": "busybox", "version": "<resolved-version>", "content_blake3": "<content-hash>"}
  ]
}
```

## Outputs and acceptance handoff

The output directory contains:

- `mere-rescue.raw`: GPT image with a 256 MiB FAT32 ESP followed by ext4.
- `mere-system-fixture.raw`: separate GPT installed-system fixture.
- `mere-system-fixture-dirty-journal.raw`: fixture copied while its root was
  mounted and a known marker was fsynced, before clean unmount.
- `manifest.json`: fixed identifiers, package inputs, tool versions, commands,
  BLAKE3 image/tree digests, and both clean-build comparisons.

The rescue ESP layout is exactly `/EFI/BOOT/BOOTX64.EFI`,
`/EFI/BOOT/limine.conf`, and `/EFI/BOOT/vmlinuz`. The generated config uses the
fixed root PARTUUID, `rootwait`, `rootflags=ro,noload`, `init=/sbin/init`, and
serial Limine branding. No BIOS, hybrid, direct-kernel, squashfs, or initramfs
artifact is assembled.

The rescue profile uses the packaged `mere-boot` dinit graph, starts mdevd
before coldplug, starts `network-dhcp` after sysfs is available, and prints
`MERE-LINUX-RESCUE-READY` on the serial console. `network-dhcp` skips `lo`, runs
BusyBox `udhcpc` on the first non-loopback interface, and uses the DHCP script
to install routes and `/etc/resolv.conf`. The image has no attached-disk
discovery service.

The assembler does not run QEMU or inspect OVMF. #649 consumes the pinned OVMF
code and fresh writable NVRAM provenance recorded alongside this manifest. #650
uses the clean and dirty fixture outputs for offline hash-preservation
acceptance.

## Local validation and dependencies

Repository-only validation does not need image privileges or host image tools:

```sh
misc-util/rescue-image-build --check
python3 -m py_compile misc-util/rescue-image-build
mere dev validate recipes/core/linux/recipe.kdl
```

Full assembly additionally requires the validated Mere profile root above and
host `mount`, `umount`, `mere`, and `tar`. The assembler uses profile-root
executables for `parted`, `mkfs.fat`/`mkfs.vfat`, `mkfs.ext4`, `losetup`,
`tune2fs`, and `debugfs`. It performs loop setup and mounts as root. It does not
silently fall back to host PATH versions when `--tool-profile-root` is supplied,
and the option is required for `--build`. Profile smoke output and direct
profile-root checks prove package availability; they do not replace the root
privilege required for image assembly.
No output is a reproducibility claim until `--compare` writes
`reproducibility.clean_builds_compared: true` and both byte-identity fields are
true in `manifest.json`.
