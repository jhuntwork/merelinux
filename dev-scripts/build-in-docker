#!/bin/sh -e

cd /src

touch /mere/pkgs/buildlocal.db
sudo pacman -Syu --noconfirm
makepkg -Ls --noconfirm
makepkg --allsource
mv ./*.src.tar.xz /mere/pkgs/

find /tmp/staging -name "*.pkg*" | while read -r file ; do
    cp -a "$file" /mere/pkgs/
    sudo pacman -Dk >/dev/null
    repo-add -R /mere/pkgs/buildlocal.db.tar.gz "/mere/pkgs/${file##*/}"
done
