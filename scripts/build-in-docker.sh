#!/bin/sh -e

cd /src

pacman -Syu --noconfirm
makepkg -Ls --noconfirm

find /tmp/staging -name "*.pkg*" | while read -r file ; do
    cp -a "$file" "/mere/pkgs/";
    pacman -Dk >/dev/null;
    repo-add -R /mere/pkgs/buildlocal.db.tar.gz "/mere/pkgs/${file##*/}";
done
