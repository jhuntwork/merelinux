#!/bin/bash
#
# NOTE:
# If running for the first time, you will need build-essential and zlib-devel 
# installed in order to compile zisofs-tools and cdrecord

# Increment for new CD releases
CDVERSION=3

# Optional param in case you have an SMP machine and wish to compress the 
# image with more threads - one per processor should be safe
if [ ! -z $1 ]  ; then
    THREADS="-p $1"
fi

# Shouldn't need to modify these
BASE=/mnt/livecd
SYSTEM=$BASE/system
ISODIR=$BASE/iso
WROOT=$BASE/work_root
ISO=$BASE/lightcubecd-$CDVERSION.iso

# Clean up from possible previous runs
umount $SYSTEM/{dev,proc,sys,tmp,}
rm -rf $SYSTEM $ISODIR $WROOT

# Exit on any errors after this point
set -e

# Working directories
install -dv $SYSTEM $ISODIR/boot/isolinux $WROOT
cd $WROOT

# Create the system image and mount it
dd if=/dev/null of=root.ext2 bs=1M seek=1536
mke2fs -F root.ext2
tune2fs -c 0 -i 0 root.ext2
mount -o loop root.ext2 $SYSTEM

# Some basic directories, nodes
install -dv $SYSTEM/{dev/shm,proc,sys,tmp}
mknod $SYSTEM/dev/console c 5 1
mknod $SYSTEM/dev/null c 1 3

# mount special file systems
mount --bind /dev $SYSTEM/dev
mount -t proc proc $SYSTEM/proc
mount -t sysfs sysfs $SYSTEM/sys
mount -t tmpfs tmpfs $SYSTEM/tmp

# install the system
smart update
smart -o remove-packages=false -o rpm-root=$SYSTEM install base-system smartmontools -y
mv -v $SYSTEM/var/lib/rpm/log.* $SYSTEM/var/lib/rpm/log
KVERSION=$(smart -o rpm-root=$SYSTEM info linux | grep Version | awk '{print $2}' | sed 's/@.*//')
chroot $SYSTEM /usr/bin/mkinitramfs $KVERSION cd $CDVERSION
install -vm0644 $SYSTEM/tmp/initramfs.gz $ISODIR/boot/isolinux/
install -vm0644 $SYSTEM/boot/vmlinux-$KVERSION $ISODIR/boot/isolinux/vmlinux

# Configure the installed system
wget -q http://dev.lightcube.us/projects/lightcubeos/repository/raw/lightcube_os/trunk/livecd/{76-network.rules,dhcp-helper,fstab,inittab,livecd-login,isolinux.cfg}
sed -i "s/__VERSION__/$CDVERSION/" livecd-login
install -vm0755 livecd-login $SYSTEM/bin/
install -vm0644 76-network.rules $SYSTEM/etc/udev/rules.d/
install -vm0755 dhcp-helper $SYSTEM/lib/udev/
install -vm0644 inittab $SYSTEM/etc/
install -vm0644 fstab $SYSTEM/etc/
install -vm0644 isolinux.cfg $ISODIR/boot/isolinux/
cp $SYSTEM/usr/share/zoneinfo/UTC $SYSTEM/etc/localtime
echo 'UTC=1' >$SYSTEM/etc/sysconfig/clock
echo 'HOSTNAME=lightcubecd' >$SYSTEM/etc/sysconfig/network
echo '127.0.0.1 localhost localhost.localdomain lightcubecd' >$SYSTEM/etc/hosts
sed -i 's@checkfs@@' $SYSTEM/etc/init.d/mountfs
chroot $SYSTEM /usr/sbin/remove_initd checkfs
chroot $SYSTEM /usr/sbin/remove_initd sshd
chroot $SYSTEM /usr/sbin/remove_initd ntpd
chroot $SYSTEM /usr/sbin/remove_initd fcron
chroot $SYSTEM /usr/sbin/remove_initd random
chroot $SYSTEM /usr/sbin/remove_initd sysklogd
chroot $SYSTEM /usr/sbin/remove_initd checkfs
chroot $SYSTEM /usr/sbin/create-cracklib-dict /usr/share/dict/cracklib-words
chroot $SYSTEM /usr/sbin/pwconv
chroot $SYSTEM /usr/sbin/grpconv

# Build some required tools, if necessary
# zisofs-tools
if [ ! -f $BASE/tools/bin/mkzftree ] ; then
    wget http://www.kernel.org/pub/linux/utils/fs/zisofs/zisofs-tools-1.0.8.tar.bz2
    tar -xf zisofs-tools-1.0.8.tar.bz2
    cd zisofs-tools-1.0.8
    ./configure --prefix=$BASE/tools
    make
    make install
    cd ..
fi

# cdrtools
if [ ! -f $BASE/tools/bin/mkisofs ] ; then
    wget ftp://ftp.berlios.de/pub/cdrecord/cdrtools-3.00.tar.bz2
    tar -xf cdrtools-3.00.tar.bz2
    cd cdrtools-3.00
    make INS_BASE=$BASE/tools DEFINSUSR=root DEFINSGRP=root
    make INS_BASE=$BASE/tools DEFINSUSR=root DEFINSGRP=root install
    cd ..
fi

# Syslinux
if [ ! -f $BASE/tools/bin/isolinux.bin ] ; then
    wget http://www.kernel.org/pub/linux/utils/boot/syslinux/syslinux-4.03.tar.bz2
    tar -xf syslinux-4.03.tar.bz2
    install -vm0644 syslinux-4.03/core/isolinux.bin $BASE/tools/bin/
fi
install -vm0644 $BASE/tools/bin/isolinux.bin $ISODIR/boot/isolinux/

# Umount the image, check the filesystem, compress the image, build the iso
umount $SYSTEM/{dev,proc,sys,tmp,}
e2fsck -f -p root.ext2 || /bin/true
echo '
Compressing the image. This may take several minutes...
'
$BASE/tools/bin/mkzftree $THREADS -F root.ext2 $ISODIR/root.ext2
cd $ISODIR
rm -f $ISO
$BASE/tools/bin/mkisofs -z -R -l --allow-leading-dots -D -o $ISO \
  -b boot/isolinux/isolinux.bin -c boot/boot.cat -no-emul-boot -boot-load-size 4 -boot-info-table \
  -V "lightcubecd-$CDVERSION" ./
echo "
ISO created: $ISO
"
