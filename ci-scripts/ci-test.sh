#!/bin/sh -e
# shellcheck disable=SC2154,SC1091
. "$CIRCLE_WORKING_DIRECTORY"/.env
if [ -n "$pkg" ] && [ -f "$pkg/PKGTEST" ]; then
  cd "$pkg"
  sh PKGTEST
fi
