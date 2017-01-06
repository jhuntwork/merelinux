#!/bin/sh
[ -d /pkgs ] || mkdir /pkgs
touch /pkgs/buildlocal.db
template=merebuild
root=/var/lib/lxc/${template}/rootfs
for file in $(find $root/merebuild/staging -name "*.pkg.*" | xargs) ; do
    cp $file /pkgs/
    repo-add -R /pkgs/buildlocal.db.tar.gz /pkgs/${file##*/}
done
