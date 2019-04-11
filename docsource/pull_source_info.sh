#!/bin/bash
pkgname=$1

dir_name=${0%/*}
if [ -d "$dir_name" ] ; then
    cd "$dir_name" || exit 1
fi

pkgdir="../packages/${pkgname}"
if [ -d "$pkgdir" ] ; then
    # shellcheck disable=SC1090
    . "${pkgdir}/PKGBUILD"
fi

# shellcheck disable=SC2154
printf '{"pkgname": "%s", "version": "%s", "url": "%s", "sha256sum": "%s", "description": "%s", "rationale": "%s", "note": "%s"}' \
    "$pkgname" "$pkgver" "${source[0]}" "${sha256sums[0]}" "$pkgdesc" "$rationale" "$note"
