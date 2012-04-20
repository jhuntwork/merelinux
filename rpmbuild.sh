#!/bin/bash

set -e

wdir=`dirname $(readlink -f $0)`

# Build an rpm in a known-sterile chroot environment using the name of the spec
# file as the mountpoint.

printhelp () {
  [ -n "${1}" ] && echo -e "\nUnknown option: $1"
  echo -e "
Usage: $0 [specfile]\n
[specfile] = \tThe name of the spec file you want to build (full path required
\tif it is not in the current directory)
"
  exit 1
}

source_spec() {
  missingfile=0
  subs=""
  name=$(grep '^Name: ' ${fullspec} | awk '{print $2}')
  version=$(grep '^Version: ' ${fullspec} | awk '{print $2}')
  release=$(grep '^Release: ' ${fullspec} | awk '{print $2}')
  arch=$(grep '^Buildarch: ' ${fullspec} | awk '{print $2}')
  arch=${arch:-$(uname -m)}
  subpkgs=$(grep '^%package ' ${fullspec} | awk '{print $2}')
}

move_files() {
  FILES="/usr/src/rpm/RPMS/${arch}/${name}-${version}-${release}.${arch}.rpm"
  FILES="${FILES} /usr/src/rpm/SRPMS/${name}-${version}-${release}.src.rpm"
  if [ ! -z "${subpkgs}" ] ; then
    for ipkg in ${subpkgs} ; do
      subs="${subs} ${ipkg}";
      FILES="${FILES} /usr/src/rpm/RPMS/${arch}/${name}-${ipkg}-${version}-${release}.${arch}.rpm"
    done
  fi
  for file in ${FILES} ; do
    if [ ! -f "/mnt/${pkg}/${file}" ] ; then
      echo "No such file or directory: /mnt/${pkg}/${file}"
      missingfile=1
    fi
  done
  if [ "${missingfile}" = "1" ] ; then
    exit 1
  else
    for file in ${FILES} ; do
      install -d "$(dirname ${file})"
      mv {"/mnt/${pkg}",}"${file}"
    done
  fi
}

[ $# -lt 1 ] || [ $# -gt 1 ] && printhelp

if ! file -i "${1}" |grep -q text; then
    echo "${1}: Not a valid spec file" >/dev/stderr
    printhelp
else
    fullspec="${1}"
    deps=$(grep ^BuildRequires.*: ${fullspec} | sed -e 's@digest.*@@' -e 's@.*Requires.*:@@' -e 's@.*%.*@@')
    spec="$(basename "${1}")"
    specdir="$(dirname "${1}")"
    # Big assumption that the specfile is named <something>.spec
    pkg=${spec%.spec}
fi

[ -z "${deps}" ] && deps=""

set -u

# Check the various mountpoints that might be in use
umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:
# Remove the chroot directory
rm -rf /mnt/"${pkg}"

# Update package library
smart update

# Setup the new chroot directory and mounts
mkdir -p /mnt/"${pkg}"/{proc,sys,dev}
mount --bind /dev /mnt/"${pkg}"/dev
mount "${pkg}"proc -t proc  /mnt/"${pkg}"/proc
mount "${pkg}"sys  -t sysfs /mnt/"${pkg}"/sys

# Install the required dependencies
#cd /mnt/"${pkg}" && tar -xvf "${wdir}/buildenv.tar.bz2" && cd "${wdir}"
smart -o remove-packages=false -o rpm-root=/mnt/"${pkg}" install \
  build-essential \
  gdb \
  strace \
  ${deps} -y

# Necessary mods to the chroot env
rm -f /mnt/"${pkg}"/bin/sh
ln -s bash /mnt/"${pkg}"/bin/sh
cp /etc/resolv.conf /mnt/"${pkg}"/etc
cp /etc/hosts /mnt/"${pkg}"/etc
#sed '/wordsize\.h/d' /usr/include/sys/debugreg.h >/mnt/"${pkg}"/usr/include/sys/debugreg.h

source_spec

# Don't rely on rpm's sketchy fetching ability, use wget or curl to fetch Source
sources=` grep -e '^Patch*' -e '^Source*' "${fullspec}" | sed -e "s@%{name}@${name}@g" -e "s@%{version}@${version}@g" | awk '{print $NF}'`
install -d "/mnt/${pkg}/usr/src/rpm/SOURCES"
install -d "/mnt/${pkg}/usr/src/rpm/BUILD"
install -d "/tmp/source-cache"
for source in $sources
do
   if echo "$source" | grep -E 'tp[s]?://' ; then
     wget -P /tmp/source-cache -c "$source"
   fi
   file=`basename $source`
   cp -a "/tmp/source-cache/$file" "/mnt/${pkg}/usr/src/rpm/SOURCES"
done

# Used to do below, but relies on rpm-build installed and configured host-system
# Instead just adjust %{PMFLAGS}, which at the moment should be the only change needed
#cp /etc/rpm/macros /mnt/"${pkg}"/etc/rpm/
cpus=`cat /proc/cpuinfo | grep processor | wc -l`
sed -i "/PMFLAGS/s@-j.*@-j$cpus@" /mnt/"${pkg}"/etc/rpm/macros

# Copy the spec file to the chroot directory and build it
cp "${fullspec}" /mnt/"${pkg}"/"${spec}"
time chroot /mnt/"${pkg}" rpm -ba "${spec}" 2>&1 | tee "${specdir}"/"${pkg}"-build.log
[ "$PIPESTATUS" -ne "0" ] && false

# Cleanup the mounts
umount /mnt/"${pkg}"/{proc,sys,dev} 2>/dev/null ||:

move_files

echo
echo "All done! The rpms are in:
/usr/src/rpms/{S,}RPMS/"
echo

read -p "Delete /mnt/${pkg}? (Will default to N in 20 seconds) (N/y) " -t 20 answer
if [ "${answer}" = "y" -o "${answer}" = "Y" ] ; then
  rm -rf "/mnt/${pkg}"
fi

# vim:ts=2:
