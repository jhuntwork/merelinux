"""Offline package inputs for the lifecycle scenario; no guest mounts on the host."""
import hashlib
from pathlib import Path
import shutil
import subprocess


def prepare(mere, root, inputs, here):
    headers = subprocess.check_output(["readelf", "-l", str(mere)])
    (inputs / "mere.elf").write_bytes(headers)
    if b"INTERP" in headers:
        raise RuntimeError("Lifecycle tests require a static ELF Mere binary")
    (root / "opt").mkdir()
    shutil.copy2(mere, root / "opt/mere")
    repositories = list((root / "mere/cache/repos").glob("*/repo.db"))
    if len(repositories) != 1:
        raise RuntimeError("Lifecycle tests expect the single public repository")
    mirror = root / "guest-repo"
    (mirror / "packages").mkdir(parents=True)
    for source in [repositories[0], Path(str(repositories[0]) + ".sig")]:
        shutil.copy2(source, mirror / source.name)
    for source in (root / "mere/cache/packages").glob("*.pkg.tar.zst"):
        shutil.copy2(source, mirror / "packages" / source.name)
    config = root / "mere/config.kdl"
    text = config.read_text()
    url = "https://pkgs.merelinux.org/mere"
    if text.count(url) != 1:
        raise RuntimeError("Expected public repository URL in lifecycle configuration")
    text = text.replace(url, "file:///guest-repo")
    config.write_text(text)
    (inputs / "guest-config.kdl").write_text(text)
    with (inputs / "guest-repo.sha256").open("w") as output:
        for source in sorted(mirror.rglob("*")):
            if source.is_file():
                output.write(f"{hashlib.sha256(source.read_bytes()).hexdigest()}  {source.relative_to(mirror)}\n")
    shutil.copytree(here / "lifecycle-fixtures", root / "etc/lifecycle")
    shutil.copytree(here / "lifecycle-fixtures", inputs / "lifecycle-fixtures")
    shutil.copy2(here / "lifecycle.py", inputs / "lifecycle.py")
    boot_recipe = here.parent.parent / "recipes/core/mere-boot"
    shutil.copytree(boot_recipe, root / "etc/lifecycle/boot-package")
    shutil.copytree(boot_recipe, inputs / "boot-package")
