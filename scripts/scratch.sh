#!/bin/sh -e

WDIR=$(mktemp -d)

trap 'rm -rf "$WDIR"' EXIT

install -d "${WDIR}/mere/var/lib/pacman"
curl -L http://repo.merelinux.org/stable/pacman-latest-x86_64.pkg.tar.xz \
     -o "${WDIR}/pacman.tar.xz"
tar -C "$WDIR" -xf "${WDIR}/pacman.tar.xz"
"${WDIR}/bin/pacman" -Sy -r "${WDIR}/mere" --noconfirm \
    --config "${WDIR}/etc/pacman.conf" \
    base-layout pacman busybox
tar -C "${WDIR}/mere" -czf "/tmp/mere-scratch.tar.gz" .
printf '/tmp/mere-scratch.tar.gz is ready\n'
