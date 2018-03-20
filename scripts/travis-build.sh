#!/bin/sh -xe
install -d staging merebuild/logs merebuild/sources merebuild/pkgs
for file in $(git diff --name-only HEAD~1) ; do
    be=0
    if printf '%s' "$file" | grep -q '^packages/'; then
        base="${file%/*}"
        [ $be -eq 0 ] && docker pull mere/buildessential && be=1
        docker run \
            -v "$(pwd):/tmp/wd" \
            -v "$(pwd)/staging:/tmp/staging" \
            -v "$(pwd)/merebuild:/merebuild" \
            mere/build-essential \
            "cd /tmp/wd/${base} && pwd && makepkg -Ls --noconfirm"
    fi
done
