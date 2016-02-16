#!/bin/sh
template=merebuild
root=/var/lib/lxc/${template}/rootfs
for file in $(find $root/pkgs/staging -name "*.pkg.*" | xargs) ; do
    cp $file /pkgs/
    repo-add /pkgs/buildlocal.db.tar.gz /pkgs/${file##*/}
done
