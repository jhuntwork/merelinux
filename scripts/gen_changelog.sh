#!/bin/bash -e
error() {
    printf "ERROR: %s\n" "$1"
    exit 1
}

pkgdir="$1"
[ -d "$pkgdir" ] || error "Missing directory: ${pkgdir}"

cd "$pkgdir"
. PKGBUILD

[ -n "$changelog" ] || changelog='ChangeLog'

[ -n "$MERE_PACKAGER" ] || MERE_PACKAGER=$(\
    grep ^#.*Maintainer: PKGBUILD | sed 's/.*://')

date=$(date +%Y-%m-%d)
comment='Initial version'

file=$(mktemp)
printf "%s %s\n\n\t* %s-%s :\n\t%s\n" "$date" "$MERE_PACKAGER" "$pkgver" \
    "$pkgrel" "$comment" | tee "$file"
if [ -f $changelog ]; then
    cat "$changelog" >>$file
fi
mv "$file" "$changelog"
