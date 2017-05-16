#!/bin/sh
pkgdir="$1"
pkgname="$2"
[ -d "$pkgdir" ] || error "Missing directory: ${pkgdir}"
pkgdir=$(realpath "$pkgdir")
basename="${pkgdir##*/}"
name="merebuild-${basename}"
if [ -z "$2" ] ; then
    pkgname="${basename}"
fi
rootfs="/var/lib/lxc/${name}/rootfs"
sort -u "${rootfs}/tmp/missingdeps.${pkgname}" | xargs printf "        %s\n" >>"${pkgdir}/PKGBUILD"
