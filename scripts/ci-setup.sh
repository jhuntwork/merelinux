#!/bin/bash -e
pkgs=()
for file in $(git diff --name-only HEAD~1) ; do
    if printf '%s' "$file" | grep -q '^packages/.*/PKGBUILD'; then
        pkgs+=("${file%/*}")
    fi
done
printf 'pkgs is: %s\n' "${pkgs[@]}"
mapfile -t unique_pkgs < <(printf '%s\n' "${pkgs[@]}" | sort -u)
if [ "${#unique_pkgs[@]}" -gt 1 ] ; then
    printf 'More than one package directory has been changed in this commit.\n'
    exit 1
fi
printf 'unique_pkgs is: %s\n' "${unique_pkgs[@]}"
install -d "$CIRCLE_WORKING_DIRECTORY"
cat >"$CIRCLE_WORKING_DIRECTORY"/.env <<EOF
pkg='${unique_pkgs[0]}'
EOF
