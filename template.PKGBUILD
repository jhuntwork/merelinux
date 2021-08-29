#!/bin/bash
# shellcheck disable=SC2034,SC2154

pkgname=(template)
pkgver=1.2.3
pkgrel=1
pkgdesc='A description of a package'
arch=(x86_64)
url='https://github.com/software/temlate'
license=(BSD)
groups=()
depends=()
makedepends=()
options=()
changelog=ChangeLog

source=(
    "${url}/${pkgname[0]}-${pkgver}.tar.gz"
)

sha256sums=(
    cc012bc860406dcf42f64431bcd3d2fa7560c02915a601aba9cd597a39329baa
)


build() {
    # See packages/pacman/std-build-functions.sh for available custom functions
    std_build
}

package() {
    # pkgfiles is an array of relative paths found in "${pkgdirbase}/dest" to include
    pkgfiles=(
        bin/template
    )
    std_package
}
