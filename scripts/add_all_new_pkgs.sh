#!/bin/sh -e
PATH="/mere/bin:${PATH}"
pkgdir="$1"

if [ ! -d "$pkgdir" ] ; then
    printf 'Missing directory: %s\n' "${pkgdir}"
    exit 1
fi

pkgdir=$(readlink -f "$pkgdir")
name="merebuild-${pkgdir##*/}"

# shellcheck disable=SC2016
lxc-start -n "$name" -F -- /bin/env -i TERM="$TERM" HOME=/tmp/wd /bin/sh -lc \
     'find /tmp/staging -name "*.pkg*" | while read -r file ; do
        cp -a "$file" "/mere/pkgs/";
        pacman -Dk >/dev/null;
        repo-add -R /mere/pkgs/buildlocal.db.tar.gz "/mere/pkgs/${file##*/}";
      done'

lxc-destroy -n "$name"
