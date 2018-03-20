#!/bin/sh -xe
for file in $(git diff --name-only HEAD~1) ; do
    if printf '%s' "$file" | grep -q '^packages/'; then
        base="${file%/*}"
        docker run -v "$(pwd):/tmp/wd" mere/build-essential \
            "cd /tmp/wd/${base}; makepkg -Ls --noconfirm"
    fi
done
