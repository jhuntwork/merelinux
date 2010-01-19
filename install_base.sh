#!/bin/bash

# Command to install all base system packages at once
ARCH=$(uname -m)
rpm -ivh \
 /usr/src/rpm/RPMS/$ARCH/base-layout-0.1-3.$ARCH.rpm \
 /usr/src/rpm/RPMS/noarch/base-files-0.0-1.noarch.rpm \
 /usr/src/rpm/RPMS/$ARCH/glibc-2.11-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/readline-6.0-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/bash-4.0-3.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/bash-doc-4.0-3.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/perl-5.10.1-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/zlib-1.2.3-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/ncurses-5.7-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/texinfo-4.13-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/gcc-libs-4.4.2-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/gcc-c++-libs-4.4.2-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/coreutils-7.6-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/e2fsprogs-1.41.8-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/grep-2.5.4-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/inetutils-1.6-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/procps-3.2.8-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/sed-4.2.1-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/util-linux-ng-2.16-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/bzip2-1.0.5-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/diffutils-2.8.1-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/file-5.03-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/gawk-3.1.7-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/findutils-4.4.2-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/groff-1.20.1-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/gzip-1.3.13-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/db-4.7.25-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/iproute2-2.6.29-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/kbd-1.15-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/less-429-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/module-init-tools-3.10-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/psmisc-22.8-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/gdbm-1.8.3-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/man-db-2.5.5-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/noarch/man-pages-3.23-1.noarch.rpm \
 /usr/src/rpm/RPMS/noarch/iana-etc-2.30-1.noarch.rpm \
 /usr/src/rpm/RPMS/$ARCH/patch-2.5.9-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/Python-2.6.3-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/cracklib-2.8.13-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/Linux-PAM-1.1.0-2.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/shadow-4.1.4.2-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/sysklogd-1.5-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/sysvinit-2.86-1.$ARCH.rpm \
 /usr/src/rpm/RPMS/$ARCH/tar-1.22-1.$ARCH.rpm

