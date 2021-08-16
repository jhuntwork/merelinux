#!/bin/bash -e
# shellcheck disable=SC2154,SC1090
. "$CIRCLE_WORKING_DIRECTORY"/.env
if [ -n "$pkg" ] ; then
    MEREDIR="$(pwd)/.mere" ./scripts/build.sh "$pkg"
else
    printf 'No packages are required to build in this commit.\n'
fi
