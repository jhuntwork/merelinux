#!/bin/bash -e
msg() {
    printf '%s\n' "$1"
}
error () {
    msg "ERROR: $1"
    exit 1
}
pkgdir="$1"
[ -d "$pkgdir" ] || error "Missing directory: ${pkgdir}"
cd "$pkgdir"
set -o pipefail
shas=$(makepkg -g | cut -d\' -f2)
# shellcheck disable=SC2086
perl -0777 -i -pe "s/sha256sums=([^)]*)/sha256sums=(\\n$(printf '    %s\n' $shas)\\n/" \
    PKGBUILD
