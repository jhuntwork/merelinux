#!/bin/sh -e
# shellcheck disable=SC2086
pacman -Syu git --noconfirm
install -d /mere/logs /mere/sources
for file in $(git diff --name-only HEAD~1) ; do
    if printf '%s' "$file" | grep -q '^packages/.*/PKGBUILD'; then
        pkgs="${pkgs} ${file%/*}"
    fi
done
unique_pkgs=$(printf '%s\n' $pkgs | sort -u)
count=$(printf '%s\n' $unique_pkgs | wc -l)
if [ "$(printf '%d' "$count")" -gt 1 ] ; then
    printf 'More than one package directory has been changed in this commit.\n'
    exit 1
fi
if [ -n "$unique_pkgs" ] ; then
    for pkg in $unique_pkgs ; do
        cd $pkg
        makepkg -Ls --noconfirm
    done
else
    printf 'No packages are required to build in this commit.\n'
fi