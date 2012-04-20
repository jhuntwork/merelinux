#!/bin/bash

set -e

wdir=`dirname $(readlink -f $0)`

# Build an rpm in a known-sterile chroot environment using the name of the spec
# file as the mountpoint.
pkg=test
set -u

# Check the various mountpoints that might be in use
umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:
# Remove the chroot directory
rm -rf /mnt/"${pkg}"

# Setup the new chroot directory and mounts
mkdir -p /mnt/"${pkg}"/{proc,sys,dev}
mount --bind /dev /mnt/"${pkg}"/dev
mount "${pkg}"proc -t proc  /mnt/"${pkg}"/proc
mount "${pkg}"sys  -t sysfs /mnt/"${pkg}"/sys

# Install the required dependencies
#cd /mnt/"${pkg}" && tar -xvf "${wdir}/buildenv.tar.bz2" && cd "${wdir}"
smart update
smart -o remove-packages=false -o rpm-root=/mnt/"${pkg}" install base-system build-essential gdb strace openssl-devel -y

cp /etc/resolv.conf /mnt/"${pkg}"/etc
cp /etc/hosts /mnt/"${pkg}"/etc
cp /usr/lib/smart/distro.py /mnt/"${pkg}"/usr/lib/smart/

#umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:
