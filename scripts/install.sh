#!/bin/sh -e
ROOT=/tmp/image/mnt

install -d "${ROOT}/var/lib/pacman"
yes | pacman -Scc
pacman -Sy --needed --noconfirm -r "${ROOT}" \
    base-layout \
    busybox-static \
    dropbear \
    execline \
    linux \
    mksh \
    nginx \
    pacman \
    s6

install -d "${ROOT}/boot/extlinux"
cat >"${ROOT}/boot/extlinux/extlinux.conf" <<EOF
SERIAL 0
DEFAULT linux

LABEL linux
  KERNEL /boot/vmlinux
  APPEND root=/dev/sda1 quiet
EOF
extlinux -i "${ROOT}/boot/extlinux"

chroot "${ROOT}" /bin/passwd

clear >"${ROOT}"/etc/issue
cat >>"${ROOT}"/etc/issue <<EOF

 mere linux 1.0 | \m \r


EOF

printf "test-%s\n" $(date +%Y%m%d%H%M%S) >"${ROOT}/etc/hostname"

touch "${ROOT}/var/log/lastlog"
rm "${ROOT}/var/log/pacman.log"

cat >"${ROOT}/etc/network/interfaces" <<EOF
auto lo eth0

iface lo inet loopback

iface eth0 inet dhcp
EOF

#sed -i "s@^exec.*@ifconfig eth0 mtu 1460\n&@" "${ROOT}/sbin/init"
