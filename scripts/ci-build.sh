#!/bin/bash -e
# shellcheck disable=SC2154,SC1090
bn="$(git rev-parse --abbrev-ref HEAD)"
if [ "$bn" != 'master' ] ; then
    . "$CIRCLE_WORKING_DIRECTORY"/.env
    if [ -n "$pkg" ] && [ "$is_deleted" = 'false' ]; then
        MEREDIR="$(pwd)/.mere" ./scripts/build.sh "$pkg"
    else
        printf 'No packages are required to build in this commit.\n'
    fi
fi
