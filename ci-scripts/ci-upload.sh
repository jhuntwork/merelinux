#!/bin/bash -xe
bn="$(git rev-parse --abbrev-ref HEAD)"
case "$bn" in
    main)
        prnum=$(git log --oneline -1 | grep -o 'Merge pull request.*from' | \
                cut -d' ' -f4 | sed 's@#@@')
        if ! printf '%d' "$prnum" >/dev/null 2>&1 ; then
            printf 'Cannot determine an upload path for the merged PR\n'
            exit 1
        fi

        # install pacman-build
        install -d /tmp/pacman
        curl -LO http://pkgs.merelinux.org/stable/pacman-latest-x86_64.pkg.tar.xz
        tar -C /tmp/pacman -xf pacman-latest-x86_64.pkg.tar.xz 2>/dev/null

        install -d ./var/lib/pacman
        sudo /tmp/pacman/usr/bin/pacman -Sy --config /tmp/pacman/etc/pacman.conf \
            -r . --noconfirm pacman-build

        # Sync down existing files in the staging repo
        install -d pkgs/testing staging
        aws s3 sync s3://pkgs.merelinux.org/testing/ pkgs/testing/
        aws s3 sync "s3://pkgs.merelinux.org/${prnum}/" staging/

        # Grab the testing dbs
        curl -fsL http://pkgs.merelinux.org/testing/testing.db.tar.gz \
            -o pkgs/testing/testing.db.tar.gz
        curl -fsL http://pkgs.merelinux.org/testing/testing.files.tar.gz \
            -o pkgs/testing/testing.files.tar.gz

        # Copy over the staging files to testing
        find staging -name "*.pkg*" -not -name "*.sig" | while read -r file ; do
            mv -v "$file" pkgs/testing
            [ -f "${file}.sig" ] && mv -v "${file}.sig" pkgs/testing
            LIBRARY=./usr/share/makepkg ./usr/bin/repo-add -R pkgs/testing/testing.db.tar.gz "pkgs/testing/${file##*/}"
        done
        find staging -name "*.src.tar.xz" | while read -r file; do
            bn=${file##*/}
            noext=${bn%.src.tar.xz*}
            norel=${noext%-*}
            nover=${norel%-*}
            find pkgs/testing -not -type d -name "${nover}*.src.tar.xz" -delete
            mv -v "$file" pkgs/testing
        done

        aws s3 sync --delete pkgs/testing/ s3://pkgs.merelinux.org/testing/
        aws s3 rm --recursive "s3://pkgs.merelinux.org/${prnum}/"
        ;;
    *)
        prnum=$(printf '%s' "$CIRCLE_PULL_REQUEST" | awk -F/ '{print $NF}')
        if [ -z "$prnum" ] || ! printf '%d' "$prnum" >/dev/null 2>&1 ; then
            printf 'Cannot determine an upload path for the merged PR\n'
            exit 1
        fi

        install -d "ci/${prnum}"
        if [ -d "/tmp/.mere/pkgs" ] ; then
            sudo find "/tmp/.mere/pkgs" -type f -exec mv -v '{}' "ci/${prnum}/" \;
            rsync -rlptv \
                -e 'ssh pkgsync@pkgs.merelinux.org -p 50220 nc localhost 873' \
                ci pkgsync@pkgs.merelinux.org::all
        fi
        ;;
esac
