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

MEREDIR="${MEREDIR:-${HOME}/.mere}"
install -d "${MEREDIR}/logs"
install -d "${MEREDIR}/pkgs"
install -d "${MEREDIR}/sources"

cmd=/usr/local/bin/build-in-docker
[ -n "$1" ] && cmd="$1"

case "$cmd" in
    gen|gen_changelog|gen_sums)
        uid=$(id -u)
        gid=$(id -g)
        toplevel=$(git rev-parse --show-toplevel)
        cp "${toplevel}/packages/base-layout/passwd" "$MEREDIR"
        cp "${toplevel}/packages/base-layout/group" "$MEREDIR"

        printf 'merebuild:x:%s:%s:Mere Build User,,,:/src:/bin/sh\n' \
            "$uid" "$gid" >>"${MEREDIR}/passwd"
        printf 'merebuild:x:%s:merebuild\n' \
            "$gid" >>"${MEREDIR}/group"

        docker run -it --rm \
            -v "$pkgdir":/src \
            -v "$MEREDIR":/mere \
            -v "$(pwd)"/dev-scripts:/usr/local/bin \
            -v "$(pwd)"/packages/pacman/pacman-dev.conf:/etc/pacman.conf \
            -v "${MEREDIR}/passwd":/etc/passwd \
            -v "${MEREDIR}/group":/etc/group \
            -u "${uid}:${gid}" \
            mere/dev:latest "$cmd"
        ;;
    *)
        tmpdir=$(mktemp -d -t "${pkgdir##*/}-XXXXXX")
        cd "$pkgdir"
        find . | cpio -dump "$tmpdir" 2>/dev/null
        cd - >/dev/null
        trap 'printf "\nBuild directory was: %s\n" $tmpdir' EXIT
        docker run -it --rm \
            -v "$tmpdir":/src \
            -v "$MEREDIR":/mere \
            -v "$(pwd)"/dev-scripts:/usr/local/bin \
            -v "$(pwd)"/packages/pacman/pacman-dev.conf:/etc/pacman.conf \
            mere/dev:latest "$cmd"
        printf '\nNew package(s) added to %s\n' "${MEREDIR}/pkgs"
        printf 'Build logs are located at %s\n' "${MEREDIR}/logs"
        ;;
esac
