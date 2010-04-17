#!/bin/bash

ARCH=$(uname -m)
REPOS="/usr/src/rpm/RPMS"

rpm -ivh -r /mnt/tempsystem \
  $REPOS/$ARCH/binutils-2.20.1-2.$ARCH.rpm \
  $REPOS/$ARCH/glibc-devel-2.11.1-2.$ARCH.rpm \
  $REPOS/$ARCH/linux-headers-2.6.33.2-1.$ARCH.rpm \
  $REPOS/$ARCH/gcc-4.4.3-2.$ARCH.rpm \
  $REPOS/$ARCH/gcc-c++-4.4.3-2.$ARCH.rpm \
  $REPOS/$ARCH/gettext-0.17-1.$ARCH.rpm \
  $REPOS/$ARCH/make-3.81-1.$ARCH.rpm \
  $REPOS/noarch/autoconf-2.65-1.noarch.rpm \
  $REPOS/noarch/automake-1.11.1-1.noarch.rpm \
  $REPOS/$ARCH/libtool-2.2.6b-1.$ARCH.rpm \
  $REPOS/$ARCH/pkg-config-0.23-1.$ARCH.rpm \
  $REPOS/$ARCH/patch-2.6.1-1.$ARCH.rpm \
  $REPOS/$ARCH/m4-1.4.14-1.$ARCH.rpm \
  $REPOS/$ARCH/flex-2.5.35-1.x86_64.rpm \
  $REPOS/$ARCH/bison-2.4.2-1.$ARCH.rpm \
  $REPOS/$ARCH/mpfr-2.4.2-1.$ARCH.rpm 
