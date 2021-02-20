#!/bin/bash -e
bn="$(git rev-parse --abbrev-ref HEAD)"
if [ "$bn" != 'master' ]; then
    printf 'Skipping for branch: %s\n' "$bn"
    exit 0
fi
pacman -Syu --noconfirm python
pip install awscli

install -d pkgs/testing
curl -fsL http://pkgs.merelinux.org/testing/main.db.tar.gz \
    -o pkgs/testing/main.db.tar.gz
curl -fsL http://pkgs.merelinux.org/testing/main.files.tar.gz \
    -o pkgs/testing/main.files.tar.gz

sed -i '/bsdtar -xf .*dbfile/s@-C@--no-fflags -C@' /bin/repo-add
find /tmp/staging -name "*.src.tar.xz" -exec mv '{}' pkgs/testing/ \;
find /tmp/staging -name "*.pkg*" | while read -r file ; do
    mv "$file" pkgs/testing
    repo-add pkgs/testing/main.db.tar.gz "pkgs/testing/${file##*/}"
done

aws s3 sync pkgs s3://pkgs.merelinux.org
