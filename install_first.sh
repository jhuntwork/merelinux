#!/bin/bash

ARCH=$(uname -m)
REPOS="/usr/src/rpm/RPMS"
#EXTRA="-r /mnt/tempsystem"

# Command to install all base system packages at once
rpm $EXTRA --initdb
rpm -qa $EXTRA
rpm -ivh $EXTRA \
 $REPOS/$ARCH/base-layout-0.1-5.$ARCH.rpm \
 $REPOS/noarch/base-files-0.1-1.noarch.rpm \
 $REPOS/$ARCH/glibc-2.11.1-2.$ARCH.rpm \
 $REPOS/$ARCH/readline-6.1-2.$ARCH.rpm \
 $REPOS/$ARCH/bash-4.1-3.$ARCH.rpm \
 $REPOS/$ARCH/zlib-1.2.4-2.$ARCH.rpm \
 $REPOS/$ARCH/ncurses-5.7-3.$ARCH.rpm \
 $REPOS/$ARCH/perl-5.10.1-1.$ARCH.rpm \
 $REPOS/$ARCH/texinfo-4.13a-1.$ARCH.rpm
rpm -qa $EXTRA
