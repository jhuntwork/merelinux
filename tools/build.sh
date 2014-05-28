#!/bin/sh -e
ROOT=/tmp/root

cleanup() {
    printf "Executing cleanup\n"
    umount "${ROOT}/dev" &&
    umount "${ROOT}/proc" &&
    umount "${ROOT}/sys" &&
    rm -rf "${ROOT}"
}

trap cleanup INT EXIT

install -d "${ROOT}/var/lib/pacman"
pacman -Sy -c --noconfirm
pacman -Sy --noconfirm -r "${ROOT}" base-layout build-essential

mount -t proc proc "${ROOT}/proc"
mount -t sysfs sysfs "${ROOT}/sys"
mount -t devtmpfs devtmpfs "${ROOT}/dev"

ln -s /proc/mounts "${ROOT}/etc/mtab"

cp /etc/pacman.conf "${ROOT}/etc/"

cp -a "$1" "${ROOT}/BUILD_PKG"

chroot "${ROOT}" /bin/sh -c "cd /BUILD_PKG && makepkg -fs --asroot --noconfirm"

install -d /tmp/pkgs
cp ${ROOT}/BUILD_PKG/*pkg.tar.xz /tmp/pkgs/

