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
    pacman \
    s6 \
    sed

install -d "${ROOT}/boot/extlinux"
cat >"${ROOT}/boot/extlinux/extlinux.conf" <<EOF
SERIAL 0
DEFAULT linux

LABEL linux
  KERNEL /boot/vmlinux
  APPEND root=/dev/sda1 console=tty0 console=ttyS0
EOF
extlinux -i "${ROOT}/boot/extlinux"

chroot "${ROOT}" /bin/passwd

printf "test-%s\n" $(date +%Y%m%d%H%M%S) >"${ROOT}/etc/hostname"

touch "${ROOT}/var/log/lastlog"
rm "${ROOT}/var/log/pacman.log"

# Make sure dropbear is started
ln -s ../etc/services/dropbear ${ROOT}/service/

cat >"${ROOT}/etc/network/interfaces" <<EOF
auto lo eth0

iface lo inet loopback

iface eth0 inet dhcp
EOF

#sed -i "s@^exec.*@ifconfig eth0 mtu 1460\n&@" "${ROOT}/sbin/init"
