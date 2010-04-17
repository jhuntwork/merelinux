#!/bin/bash

ARCH=$(uname -m)
REPOS="/usr/src/rpm/RPMS"
EXTRA="-r /mnt/tempsystem"

rpm -ivh $EXTRA \
 $REPOS/$ARCH/bash-doc-4.1-3.$ARCH.rpm \
 $REPOS/$ARCH/gcc-libs-4.4.3-2.$ARCH.rpm \
 $REPOS/$ARCH/gcc-c++-libs-4.4.3-2.$ARCH.rpm \
 $REPOS/$ARCH/coreutils-8.4-2.$ARCH.rpm \
 $REPOS/$ARCH/gmp-5.0.1-2.$ARCH.rpm \
 $REPOS/$ARCH/e2fsprogs-1.41.11-1.$ARCH.rpm \
 $REPOS/$ARCH/grep-2.6.1-1.$ARCH.rpm \
 $REPOS/$ARCH/inetutils-1.7-1.$ARCH.rpm \
 $REPOS/$ARCH/procps-3.2.8-1.$ARCH.rpm \
 $REPOS/$ARCH/sed-4.2.1-2.$ARCH.rpm \
 $REPOS/$ARCH/util-linux-ng-2.17.2-1.$ARCH.rpm \
 $REPOS/$ARCH/bzip2-1.0.5-2.$ARCH.rpm \
 $REPOS/$ARCH/diffutils-2.9-1.$ARCH.rpm \
 $REPOS/$ARCH/file-5.04-1.$ARCH.rpm \
 $REPOS/$ARCH/gawk-3.1.7-2.$ARCH.rpm \
 $REPOS/$ARCH/findutils-4.4.2-2.$ARCH.rpm \
 $REPOS/$ARCH/groff-1.20.1-2.$ARCH.rpm \
 $REPOS/$ARCH/gzip-1.4-1.$ARCH.rpm \
 $REPOS/$ARCH/iproute2-2.6.33-2.$ARCH.rpm \
 $REPOS/$ARCH/kbd-1.15.1-1.$ARCH.rpm \
 $REPOS/$ARCH/less-436-1.$ARCH.rpm \
 $REPOS/$ARCH/gdbm-1.8.3-1.$ARCH.rpm \
 $REPOS/noarch/man-pages-3.24-1.noarch.rpm \
 $REPOS/noarch/iana-etc-2.30-1.noarch.rpm \
 $REPOS/$ARCH/psmisc-22.10-2.$ARCH.rpm \
 $REPOS/$ARCH/sysklogd-1.5-1.$ARCH.rpm \
 $REPOS/$ARCH/tar-1.23-1.$ARCH.rpm \
 $REPOS/$ARCH/cracklib-2.8.16-2.$ARCH.rpm \
 $REPOS/$ARCH/Linux-PAM-1.1.1-1.$ARCH.rpm \
 $REPOS/$ARCH/shadow-4.1.4.2-1.$ARCH.rpm \
 $REPOS/$ARCH/module-init-tools-3.11.1-1.$ARCH.rpm \
 $REPOS/$ARCH/man-db-2.5.7-1.$ARCH.rpm \
 $REPOS/noarch/lfs-bootscripts-20100124-1.noarch.rpm \
 $REPOS/$ARCH/beecrypt-4.2.1-1.$ARCH.rpm \
 $REPOS/$ARCH/vim-7.2-1.$ARCH.rpm \
 $REPOS/$ARCH/udev-151-1.$ARCH.rpm \
 $REPOS/$ARCH/pcre-8.02-1.$ARCH.rpm \
 $REPOS/$ARCH/popt-1.15-1.$ARCH.rpm \
 $REPOS/$ARCH/openssl-1.0.0-1.$ARCH.rpm \
 $REPOS/$ARCH/sysvinit-2.86-1.$ARCH.rpm \
 $REPOS/$ARCH/grub-1.98-1.$ARCH.rpm \
 $REPOS/$ARCH/expat-2.0.1-2.$ARCH.rpm \
 $REPOS/$ARCH/neon-0.29.3-1.$ARCH.rpm \
 $REPOS/$ARCH/rpm-5.1.9-2.$ARCH.rpm \
