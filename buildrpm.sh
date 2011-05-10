#!/bin/bash

set -x
set -e

# Build an rpm in a known-sterile chroot environment using the name of the spec
# file as the mountpoint.

[ -z "${1}" ] && { echo "give me a spec file to work with" >/dev/stderr; exit 1; }

set -u

pkg="${1}"

if ! file -i "${pkg}" |grep -q text/plain; then
  echo "give me a spec file to work with" >/dev/stderr
  exit 1
fi

spec=$(basename "${pkg}")

# Big assumption that the specfile is named <something>.spec
pkg=${pkg%.spec}

# Check the various mountpoints that might be in use
umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:
rm -rf /mnt/"${pkg}"

mkdir -p /mnt/"${pkg}"/{proc,sys,dev}
mount --bind /dev /mnt/"${pkg}"/dev
mount "${pkg}"proc -t proc  /mnt/"${pkg}"/proc
mount "${pkg}"sys  -t sysfs /mnt/"${pkg}"/sys
smart -o rpm-root=/mnt/"${pkg}" install base-system build-essential -y
cp /etc/resolv.conf /mnt/"${pkg}"/etc
mv /mnt/"${pkg}"/var/lib/rpm/log.* /mnt/"${pkg}"/var/lib/rpm/log

cp "${1}" /mnt/"${pkg}"/"${spec}"

chroot /mnt/"${pkg}" rpm -ba "${spec}" 2>&1 |tee "${pkg}"-build.log
[ "$PIPESTATUS" -ne "0" ] && false

umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:

echo "All done! The rpms are in:
/mnt/"${pkg}"/usr/src/rpms/{S,}RPMS/"
