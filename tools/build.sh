#!/bin/sh
ROOT=/tmp/root
do_clean=0
do_mount=0
do_umount=0
# type:src:dest
# if type is 1, it is the same as source
# if type is 0, there is no type
# if type is anything else, use type as defined
mounts="1:devtmpfs:/dev 1:proc:/proc 1:sysfs:/sys 0:/pkgs:/pkgs"

while getopts "mucp:" arg ; do
    case $arg in
        m) do_mount=1 ;;
        u) do_umount=1 ;;
        c) do_clean=1 ;;
        p)
            pkgdir="$OPTARG"
            if [ ! -d "$pkgdir" ] ; then
                printf "Missing directory: %s\n" $pkgdir
                exit 1
            fi
            ;;
    esac
done

is_mounted() {
    awk {'print $2'} /proc/mounts | grep -q "^$@$"
    return $?
}

cleanup() {
    if [ $1 -eq 1 ] ; then
        umount_virtual
        printf "Cleaning %s\n" "$ROOT"
        rm -rf "$ROOT"
    fi
}

mount_virtual() {
    printf "Mounting virtual file systems\n"
    for mount in $mounts ; do
        dest=${ROOT}${mount##*:}
        src=$(echo $mount | cut -d: -f2)
        type=$(echo $mount | cut -d: -f1)
        case $type in
            0) is_mounted "$dest" || mount "$src" "$dest" ;;
            1) is_mounted "$dest" || mount -t "$src" "$src" "$dest" ;;
            *) is_mounted "$dest" || mount -t "$type" "$src" "$dest" ;;
        esac
    done
}

umount_virtual() {
    printf "Unmounting virtual file systems\n"
    for mount in $mounts ; do
        dest=${ROOT}${mount##*:}
        is_mounted "$dest" && umount "$dest"
    done
}

trap "cleanup ${do_clean}" INT EXIT

if [ $do_mount -eq 1 ] ; then
    mount_virtual && exit 0
fi

if [ $do_umount -eq 1 ] ; then
    umount_virtual && exit 0
fi

[ $do_clean -eq 1 ] && exit 0

if [ -z $pkgdir ] ; then
    printf "Package directory required\n"
    exit 1
fi

# Before doing anything ensure the directory is clean
cleanup 1
set -e

install -d "${ROOT}/var/lib/pacman"
install -d "${ROOT}/pkgs"
yes | pacman -Scc
pacman -Sy --noconfirm -r "$ROOT" base-layout build-essential

mount_virtual

cp /etc/resolv.conf "${ROOT}/etc/"
echo '127.0.0.1 localhost.localdomain localhost' >"${ROOT}/etc/hosts"

install -g nobody -d "${ROOT}/BUILD_PKG"
chmod g+s "${ROOT}/BUILD_PKG"
setfacl -m u::rwx,g::rwx "${ROOT}/BUILD_PKG"
setfacl -d --set u::rwx,g::rx,o::rx "${ROOT}/BUILD_PKG"
find "${pkgdir}" -maxdepth 1 -type f -exec cp '{}' "${ROOT}/BUILD_PKG/" \;
echo 'nobody ALL=NOPASSWD: /bin/pacman' >"${ROOT}/etc/sudoers.d/nobody"

chroot "${ROOT}" /bin/sudo -u nobody -- /bin/env -i \
    PATH=/bin:/sbin TERM=$TERM HOME=/BUILD_PKG \
    LC_ALL=POSIX /bin/sh -c 'cd /BUILD_PKG && makepkg -fLs --noconfirm'
