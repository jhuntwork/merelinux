#!/bin/bash -e

# Get metadata about what was just merged
prnum=$(git log --oneline -1 | grep -o 'Merge pull request.*from' | \
        cut -d' ' -f4 | sed 's@#@@')
if ! printf '%d' "$prnum" >/dev/null 2>&1 ; then
    printf 'Cannot determine the PR num\n'
    exit 1
fi
originbranch=$(git log --oneline -1 | grep -o 'Merge pull request.*from.*' | \
    awk '{print $NF}')
originuser="${originbranch%/*}"
if [ "$originuser" = "$CIRCLE_PROJECT_USERNAME" ]; then
    branch="${originbranch##*/}"
else
    branch="pull/${prnum}"
fi
[ -n "$branch" ] || { printf 'Cannot determine the origin branch name\n'; exit 1; }

# install pacman-build
install -d /tmp/pacman
curl -LO http://pkgs.merelinux.org/testing/pacman-latest-x86_64.pkg.tar.xz
tar -C /tmp/pacman -xf pacman-latest-x86_64.pkg.tar.xz 2>/dev/null

install -d /tmp/tools/var/lib/pacman
sudo /tmp/pacman/usr/bin/pacman -Sy --config /tmp/pacman/etc/pacman.conf \
    -r /tmp/tools --noconfirm pacman-build curl jq
export PATH="/tmp/tools/bin:/tmp/tools/usr/bin:$PATH"

# Download artifacts
artifacts="$(curl \
    "https://circleci.com/api/v1.1/project/github/jhuntwork/merelinux/latest/artifacts?branch=${branch}&filter=successful" \
    -H "Circle-Token: ${CIRCLE_API_TOKEN}")"
[ -n "$artifacts" ] || { printf 'Unable to find artifacts to upload\n'; exit 1; }

install -d staging
len=$(printf '%s\n' "$artifacts" | jq '. | length')
i=0
while [ "$i" -lt "$len" ]; do
    url=$(printf '%s\n' "$artifacts" | jq -r .[$i].url)
    printf 'Downloading %s\n' "$url"
    curl -LO --output-dir staging "$url"
    i=$((i+1))
done

# Sync down existing files in the testing repo
printf 'Syncing down testing repo\n'
install -d pkgs/testing
rsync -rlptv -e 'ssh -p 50220' \
    pkgsync@pkgs.merelinux.org::pkgs/testing/ pkgs/testing/

# Copy over the staging files to testing
find staging -name "*.pkg*" -not -name "*.sig" | while read -r file ; do
    mv -v "$file" pkgs/testing
    [ -f "${file}.sig" ] && mv -v "${file}.sig" pkgs/testing
    LIBRARY=/tmp/tools/usr/share/makepkg repo-add \
        --sign --key "${CIRCLE_WORKING_DIRECTORY}/mere.key" \
        -R pkgs/testing/testing.db.tar.gz "pkgs/testing/${file##*/}"
done
find staging -name "*.src.tar.xz" | while read -r file; do
    bn=${file##*/}
    noext=${bn%.src.tar.xz*}
    norel=${noext%-*}
    nover=${norel%-*}
    install -d "src/${nover}"
    mv -v "$file" "src/${nover}/"

    printf 'Syncing up source packages\n'
    rsync -rlptv --delete-after -e 'ssh -p 50220' \
        "src/${nover}/" "pkgsync@pkgs.merelinux.org::pkgs/src/${nover}/"
done

# Upload
printf 'Syncing up testing repo\n'
rsync -rlptv --delete-after -e 'ssh -p 50220' \
    pkgs/testing/ pkgsync@pkgs.merelinux.org::pkgs/testing/
