#!/bin/sh -e
ROOT=/tmp/root
clean=0

while getopts "cp:" arg ; do
    case $arg in
    	c) clean=1 ;;
    	p) pkgdir="$OPTARG" ;;
    esac
done

if [ -z "$pkgdir" ] ; then
    printf "Package directory required\n"
    exit 1
fi

is_mounted() {
    awk {'print $2'} /proc/mounts | grep -q "^$@$"
    return $?
}

cleanup() {
    printf "Unmounting virtual file systems\n"
    for mount in "${ROOT}/dev" "${ROOT}/proc" "${ROOT}/sys" ; do
        if is_mounted "$mount" ; then
            umount "$mount"
        fi
    done
    if [ $1 -eq 1 ] ; then
        printf "Cleaning %s\n" "$ROOT"
        rm -rf "$ROOT"
    fi
}

trap "cleanup ${clean}" INT EXIT

# Before doing anything ensure the directory is clean
cleanup 1

install -d "${ROOT}/var/lib/pacman"
yes | pacman -Sy -cc
pacman -Sy --noconfirm -r "${ROOT}" base-layout build-essential

mount -t proc proc "${ROOT}/proc"
mount -t sysfs sysfs "${ROOT}/sys"
mount -t devtmpfs devtmpfs "${ROOT}/dev"

ln -s /proc/mounts "${ROOT}/etc/mtab"

cp /etc/pacman.conf "${ROOT}/etc/"

cp -a "$pkgdir" "${ROOT}/BUILD_PKG"

chroot "${ROOT}" /bin/sh -c "cd /BUILD_PKG && makepkg -fs --asroot --noconfirm"

install -d /tmp/pkgs
cp ${ROOT}/BUILD_PKG/*pkg.tar.xz /tmp/pkgs/

