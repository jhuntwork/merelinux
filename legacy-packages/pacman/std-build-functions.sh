#!/bin/bash
# shellcheck disable=SC2154,SC2068
cd_unpacked_src() {
    unpacked_src=$(find "$srcdir" -maxdepth 1 -mindepth 1 -type d)
    [ "$(printf '%s\n' "$unpacked_src" | wc -l)" -eq 1 ]
    cd "$unpacked_src" || return 1
}

package_defined_files() {
    if [ -n "$1" ]; then cd "$1" || return 1; fi
    set -o pipefail
    find ${pkgfiles[@]} | cpio -dump "$pkgdir"
}

std_build() {
    cd_unpacked_src
    ./configure --prefix=/usr
    make
}

std_package() {
    cd_unpacked_src
    make DESTDIR="${pkgdirbase}/dest" install
    std_split_package
}

std_split_package() {
    package_defined_files "${pkgdirbase}/dest"
}
