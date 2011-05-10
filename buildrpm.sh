#!/bin/bash

set -e

# Build an rpm in a known-sterile chroot environment using the name of the spec
# file as the mountpoint.

printhelp () {
  [ -n "${1}" ] && echo -e "\nUnknown option: $1"
  echo -e "
Usage: $0 -s [specfile] -p <<package1>,<package2>,<package3>>\n
-s\tThe name of the spec file you want to build (full path required
\tif it is not in the current directory)
-p\tcomma-separated additional dependencies beyond base-system and
\tbuild-essential that need to be installed in the chroot
"
  exit 1
}

[ $# -lt 2 ] || [ $# -gt 4 ] && printhelp

set -- "$@" _eNd_OF_lisT_

while [ "${1}" != "_eNd_OF_lisT_" ]; do
  case $1 in
    -s)
      if ! file -i "${2}" |grep -q text/plain; then
        echo "${2}: Not a valid spec file" >/dev/stderr
				printhelp
			else
				fullspec="${2}"
				spec="$(basename "${2}")"
				# Big assumption that the specfile is named <something>.spec
				pkg=${spec%.spec}
			fi
      shift 2
      ;;
    -p)
      deps="${2//,/ }"
      shift 2
      ;;
    *)
      printhelp "${1}"
      ;;
  esac
done

[ -z "${deps}" ] && deps=""

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
smart -o rpm-root=/mnt/"${pkg}" install base-system build-essential ${deps} -y

# Some cleanup
cp /etc/resolv.conf /mnt/"${pkg}"/etc
mv /mnt/"${pkg}"/var/lib/rpm/log.* /mnt/"${pkg}"/var/lib/rpm/log

# Copy the spec file to the chroot directory and build it
cp "${fullspec}" /mnt/"${pkg}"/"${spec}"
chroot /mnt/"${pkg}" rpm -ba "${spec}" 2>&1 |tee "${pkg}"-build.log
[ "$PIPESTATUS" -ne "0" ] && false

# Cleanup the mounts
umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:

echo "All done! The rpms are in:
/mnt/"${pkg}"/usr/src/rpms/{S,}RPMS/"



# vim:ts=2:
