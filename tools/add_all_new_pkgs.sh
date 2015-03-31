#!/bin/sh
for file in $(find /tmp/root/BUILD_PKG -name "*.pkg.*" | xargs) ; do
    cp /pkgs/staging/${file##*/} /pkgs/
    repo-add /pkgs/main.db.tar.gz /pkgs/${file##*/}
done
