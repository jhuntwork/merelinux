#!/bin/bash
# shellcheck disable=SC2154,SC2068
cd_unpacked_src() {
    unpacked_src=$(find "$srcdir" -maxdepth 1 -mindepth 1 -type d)
    [ "$(printf '%s\n' "$unpacked_src" | wc -l)" -eq 1 ]
    cd "$unpacked_src" || return 1
}

package_defined_files() {
    cd "${pkgdirbase}/dest" || return 1
    set -o pipefail
    find ${pkgfiles[@]} | cpio -dump "$pkgdir"
}

std_build() {
    cd_unpacked_src
    ./configure --prefix=''
    make
}

std_package() {
    cd_unpacked_src
    make DESTDIR="${pkgdirbase}/dest" install
    package_defined_files
}

std_split_package() {
    package_defined_files
}
