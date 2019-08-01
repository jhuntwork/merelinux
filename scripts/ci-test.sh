#!/bin/sh -e
# shellcheck disable=SC2154,SC1090
. "$CIRCLE_WORKING_DIRECTORY"/.env
if [ -n "$pkg" ] ; then
  cd "$pkg"
  sh PKGTEST
fi