#!/bin/sh -xe
install -d staging build
for file in $(git diff --name-only HEAD~1) ; do
    if printf '%s' "$file" | grep -q '^packages/'; then
        build="${build} ${file%/*}"
    fi
done
# shellcheck disable=SC2086
for pkg in $(printf '%s\n' $build | sort -u) ; do
    docker run \
        -v "$(pwd)/${pkg}:/tmp/pkg" \
        -v "$(pwd)/staging:/tmp/staging" \
        -v "$(pwd)/build:/mere" \
        mere/build-essential \
        /bin/bash -c \
        'install -d /tmp/wd; cp /tmp/pkg/* /tmp/wd; cd /tmp/wd; makepkg -Ls --noconfirm'
done
