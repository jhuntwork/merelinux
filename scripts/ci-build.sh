#!/bin/bash -e
# shellcheck disable=SC2154,SC1090
. "$CIRCLE_WORKING_DIRECTORY"/.env
if [ -n "$pkg" ] ; then
    pacman -Sy
    . "$pkg"/PKGBUILD
    proposed="${pkgver}-${pkgrel}"
    current="$(pacman -Sl | grep "${pkgname} " | cut -d' ' -f3)"
    if [ "$(printf '%s\n' "$proposed" "$current" | \
            sort | tail -n1)" != "$proposed" ]; then
        printf "The proposed version '%s' appears to be less \
than the current version '%s'\n" "$proposed" "$current"
        exit 1
    fi
    install -d /mere/logs /mere/sources
    cd "$pkg"
    sed -i '/MAKEFLAGS=/s@=.*@=@' /etc/makepkg.conf
    makepkg -Ls --noconfirm
else
    printf 'No packages are required to build in this commit.\n'
fi