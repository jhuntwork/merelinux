#!/bin/bash -e
bn="$(git rev-parse --abbrev-ref HEAD)"
if [ "$bn" != 'master' ]; then
    printf 'Skipping for branch: %s\n' "$bn"
    exit 0
fi
pacman -Syu --noconfirm python
pip install awscli

install -d pkgs/stable
curl -fsL http://pkgs.merelinux.org/stable/main.db.tar.gz \
    -o pkgs/stable/main.db.tar.gz
curl -fsL http://pkgs.merelinux.org/stable/main.files.tar.gz \
    -o pkgs/stable/main.files.tar.gz

# FIXME: remove the below
sed -i '/bsdtar -xf .*dbfile/s@-C@--no-fflags -C@' /bin/repo-add
find /tmp/staging -name "*.pkg*" | while read -r file ; do
    mv "$file" pkgs/stable
    repo-add -R pkgs/stable/main.db.tar.gz "pkgs/stable/${file##*/}"
done

aws s3 sync pkgs s3://pkgs.merelinux.org
