#!/bin/bash -e
bn="$(git rev-parse --abbrev-ref HEAD)"
if [ "$bn" != 'master' ]; then
    printf 'Skipping for branch: %s\n' "$bn"
    exit 0
fi

curl -LO http://pkgs.merelinux.org/stable/pacman-latest-x86_64.pkg.tar.xz
tar -xf pacman-latest-x86_64.pkg.tar.xz
install -d ./var/lib/pacman
./bin/pacman -S --config etc/pacman.conf -y -r . --noconfirm --overwrite pacman-build

pip install awscli

install -d pkgs/testing
curl -fsL http://pkgs.merelinux.org/testing/main.db.tar.gz \
    -o pkgs/testing/main.db.tar.gz
curl -fsL http://pkgs.merelinux.org/testing/main.files.tar.gz \
    -o pkgs/testing/main.files.tar.gz

sed -i '/bsdtar -xf .*dbfile/s@-C@--no-fflags -C@' bin/repo-add
find "${HOME}/.mere/tmp/staging" -name "*.src.tar.xz" -exec mv '{}' pkgs/testing/ \;
find "${HOME}/.mere/tmp/staging" -name "*.pkg*" | while read -r file ; do
    mv "$file" pkgs/testing
    ./bin/repo-add -R pkgs/testing/main.db.tar.gz "pkgs/testing/${file##*/}"
done

aws s3 sync pkgs s3://pkgs.merelinux.org
