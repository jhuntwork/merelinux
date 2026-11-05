# Rescue image build pipeline

`misc-util/rescue-image-build` is the #648 host-side assembler. It consumes
staged Mere package trees, a staged x86_64 kernel, and the Limine EFI output. It
produces a 2 GiB GPT raw rescue image, a separate installed-system fixture, a
dirty-journal fixture, and `manifest.json`.

The assembler is deliberately fail-closed. It requires the fixed inputs in
`misc-util/rescue-image.inputs.json`, root for loop/mount operations, the pinned
image tools, and two clean-build comparisons. A single build cannot be reported
as reproducible.

The selected Mere version is `0.23.0` throughout the tool profile and build
inputs. The pinned x86_64 Mere binary SHA-256 is
`3250c04b7f288056f5db8860a644a17895a7dc6398ddc961e1316bfe928ea631`.
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

Build the non-kernel recipes through `@jeremy/mere-dev`, which invokes
`mere dev build` directly in its isolated root. The top-level command uses the
existing pinned Linux package instead of rebuilding Linux:

```sh
for recipe in \
  recipes/core/busybox/recipe.kdl \
  recipes/core/dinit/recipe.kdl \
  recipes/core/e2fsprogs/recipe.kdl \
  recipes/core/limine/recipe.kdl \
  recipes/core/mdevd/recipe.kdl \
  recipes/core/parted/recipe.kdl
do
  swamp behavior run mere-rescue-dev-023 build \
    --repo-dir "$SWAMP_REPO" --input "recipe=$PWD/$recipe"
done
```

### Isolated image-tool profile

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

The top-level `--build --compare --build-packages` path performs package
preparation and staging before assembly. It builds the pinned non-kernel
recipes through `@jeremy/mere-dev`, uses the existing pinned Linux
`6.18.42-2` package after auditing its shipped `boot/config`, stages the rescue
root and installed-system fixture, creates the fixture ESP, and writes the
package manifest. It does not rebuild Linux with a rescue-only configuration.
The kernel audit follows the real 6.18.42 configuration symbols; there is no
`CONFIG_PARTITION_ADVANCED` or `CONFIG_DEVPTS_FS` requirement in this path.

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
archive hashes are written into the firmware manifest. The profile supplies
Clang/Clang++, NASM, Make, Flex, Bison, m4, Python, and the UUID development
headers. ACPICA iasl is built from
the separately pinned ACPICA source archive above.

```sh
misc-util/rescue-image-build --build \
  --compare \
  --build-packages \
  --mere-dev-behavior mere-rescue-dev-023 \
  --swamp-repo-dir "$SWAMP_REPO" \
  --tool-profile-root "$TOOL_PROFILE_ROOT" \
  --ovmf-tool-profile-root /mere/profiles/mere-rescue-ovmf-023/root \
  --output-dir out/rescue-image
```

A representative package manifest has this shape. The package list must include
every image package and every tool-profile package:

```json
{
  "mere": {
    "version": "0.23.0",
    "binary_blake3": "<mere-binary-hash>",
    "binary_sha256": "3250c04b7f288056f5db8860a644a17895a7dc6398ddc961e1316bfe928ea631",
    "repository_snapshot": "<snapshot>"
  },
  "packages": [
    {"name": "dinit", "version": "<dinit-package-version>", "archive_blake3": "<image-package-hash>"}
  ],
  "providers": {
    "/bin/busybox": "busybox",
    "/boot/vmlinux": "linux",
    "/boot/config": "linux"
  },
  "tool_profile_packages": [
    {"name": "busybox", "version": "1.37.0-10", "archive_blake3": "<tool-package-hash>"}
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
fixed root PARTUUID, `rootwait`, `rootflags=ro,noload`, `init=/sbin/dinit`, and
serial Limine branding. No BIOS, hybrid, direct-kernel, squashfs, or initramfs
artifact is assembled.

The rescue profile mounts only virtual filesystems, starts mdevd before
coldplug, and prints `MERE-LINUX-RESCUE-READY`. It has no root remount or
attached-disk discovery service.

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
