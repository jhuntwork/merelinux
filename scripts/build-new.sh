#!/bin/sh -e
changelog="$(realpath ${1})/ChangeLog"
if [ -f "$changelog" ] ; then
    rm -f "$changelog"
fi
./tools/gen_changelog.sh $@
./tools/gen_sums.sh $@
./tools/build.sh $@
