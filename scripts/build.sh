#!/bin/sh -e

usage() {
    printf '
Usage: %s <pkgdir>

  <pkgdir>   Identifies a directory containing, at minimum, a PKGBUILD file.
             The directory may also contain a ChangeLog file and additional
             source files required for the build.
' "$0"
}

if [ -z "$1" ] || [ ! -d "$1" ] ; then
    usage
    printf 'Missing or invalid directory. pkgdir argument: %s\n' "${pkgdir}"
else
    pkgdir=$(realpath "$1")
    shift
fi

cmd=/local/bin/build-in-docker.sh
[ -n "$1" ] && cmd="$1"

docker run -it --rm \
    -v "${pkgdir}":/src \
    -v /mere/logs:/mere/logs \
    -v /mere/pkgs:/mere/pkgs \
    -v /mere/sources:/mere/sources \
    mere/dev:latest "$cmd"
