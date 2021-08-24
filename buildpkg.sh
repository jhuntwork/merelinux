#!/bin/sh -e

usage() {
    printf '
Usage: %s <pkgdir> [cmd]

  <pkgdir>   Identifies a directory containing, at minimum, a PKGBUILD file.
             The directory may also contain a ChangeLog file and additional
             source files required for the build.

  [cmd]      Optional command to run inside the container. E.g., /bin/sh.
             The default is /usr/local/bin/build-in-docker
' "$0"
}

# A really simple implementation of realpath for systems that don't have it
realpath_cd () {
    cd "$1" || return 1
    pwd -P
    cd - >/dev/null 2>&1 || return 1
}

bad_pkgdir() {
    usage
    printf '\nMissing or invalid directory: %s\n' "$1"
    exit 2
}

if [ -z "$1" ] || [ ! -d "$1" ] ; then
    bad_pkgdir "$1"
else
    rp=realpath
    command -v $rp >/dev/null || rp='realpath_cd'
    pkgdir=$($rp "$1")
    shift
fi

cmd=/usr/local/bin/build-in-docker
[ -n "$1" ] && cmd="$1"
[ -d "${pkgdir}/pkg" ] && chmod 755 "${pkgdir}/pkg"

MEREDIR="${MEREDIR:-${HOME}/.mere}"
uid=$(id -u)
gid=$(id -g)

install -d "${MEREDIR}/logs"
install -d "${MEREDIR}/pkgs"
install -d "${MEREDIR}/sources"

# These two lines assume the script will be run from the top of the merelinux
# source directory. May revisit this in the future.
cp packages/base-layout/passwd "$MEREDIR"
cp packages/base-layout/group "$MEREDIR"

if [ "$uid" = '0' ]; then
    docker run -it --rm \
        -v "$pkgdir":/src \
        -v "$MEREDIR":/mere \
        -v "$(pwd)"/dev-scripts:/usr/local/bin \
        -v "$(pwd)"/packages/pacman/pacman-dev.conf:/etc/pacman.conf \
        mere/dev:latest "$cmd"
else
    printf 'merebuild:x:%s:%s:Mere Build User,,,:/src:/bin/sh\n' \
        "$uid" "$gid" >>"${MEREDIR}/passwd"
    printf 'merebuild:x:%s:merebuild\n' \
        "$gid" >>"${MEREDIR}/group"

    docker run -it --rm \
        -e PACKAGER="$MERE_PACKAGER" \
        -v "$pkgdir":/src \
        -v "$MEREDIR":/mere \
        -v "${MEREDIR}/passwd":/etc/passwd \
        -v "${MEREDIR}/group":/etc/group \
        -v "$(pwd)"/packages/pacman/pacman-dev.conf:/etc/pacman.conf \
        -v "$(pwd)"/dev-scripts:/usr/local/bin \
        -u "${uid}:${gid}" \
        mere/dev:latest "$cmd"
fi
