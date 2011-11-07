Summary: Util-Linux Next Generation
Name: util-linux
Version: 2.20
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/util-linux
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

Obsoletes: util-linux-ng
BuildRequires: digest(sha1:%{SOURCE0}) = e8cd2c8e968cdbdc097d82cceaf15d536e0254c1
BuildRequires: ncurses-devel
BuildRequires: zlib-devel

%description
Provides some core Linux utilities, particularly those
relating to the file system.

%package devel
Summary: %{name} headers and libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for libblkid and libuuid

%prep
%setup -q
sed -i 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)

%build
export CFLAGS='-Os -pipe'
./configure \
  --enable-arch \
  --enable-partx \
  --enable-write \
  --libdir=/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}/usr/share/info/dir
rm %{buildroot}/usr/share/getopt/*.tcsh
install -dv %{buildroot}/var/lib/hwclock
# Spurious man page - binary not built
rm -f %{buildroot}/usr/share/man/ru/man1/ddate.1
%{compress_man}
%{strip}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/bin/arch
/bin/dmesg
/bin/lsblk
/bin/more
/bin/mount
/bin/mountpoint
/bin/umount
/bin/findmnt
/%{_lib}/libmount.so.1
/%{_lib}/libmount.so.1.1.0
/%{_lib}/libblkid.so.*
/%{_lib}/libuuid.so.*
/sbin/agetty
/sbin/fsfreeze
/sbin/fstrim
/sbin/swaplabel
/sbin/blkid
/sbin/blockdev
/sbin/cfdisk
/sbin/ctrlaltdel
/sbin/fdisk
/sbin/findfs
/sbin/fsck
/sbin/fsck.cramfs
/sbin/fsck.minix
/sbin/hwclock
/sbin/losetup
/sbin/mkfs
/sbin/mkfs.bfs
/sbin/mkfs.cramfs
/sbin/mkfs.minix
/sbin/mkswap
/sbin/pivot_root
/sbin/sfdisk
/sbin/swapoff
/sbin/swapon
/sbin/switch_root
/sbin/wipefs
/usr/bin/cal
/usr/bin/chkdupexe
/usr/bin/chrt
/usr/bin/col
/usr/bin/colcrt
/usr/bin/colrm
/usr/bin/column
/usr/bin/cytune
/usr/bin/fallocate
/usr/bin/flock
/usr/bin/getopt
/usr/bin/hexdump
/usr/bin/ionice
/usr/bin/ipcmk
/usr/bin/ipcrm
/usr/bin/ipcs
/usr/bin/isosize
/usr/bin/linux32
/usr/bin/linux64
/usr/bin/logger
/usr/bin/look
/usr/bin/lscpu
/usr/bin/mcookie
/usr/bin/namei
/usr/bin/pg
/usr/bin/rename
/usr/bin/renice
/usr/bin/rev
/usr/bin/script
/usr/bin/scriptreplay
/usr/bin/setarch
/usr/bin/setsid
/usr/bin/setterm
/usr/bin/tailf
/usr/bin/taskset
/usr/bin/ul
/usr/bin/unshare
/usr/bin/uuidgen
/usr/bin/wall
/usr/bin/whereis
/usr/bin/write
/usr/sbin/addpart
/usr/sbin/delpart
/usr/sbin/fdformat
/usr/sbin/ldattach
/usr/sbin/partx
/usr/sbin/readprofile
/usr/sbin/rtcwake
/usr/sbin/tunelp
/usr/sbin/uuidd
/usr/share/getopt
/usr/share/man/man1/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man8/*.bz2
%ifarch i686
/usr/bin/i386
%endif
%ifarch ppc
/usr/bin/ppc
/usr/bin/ppc32
/usr/bin/ppc64
%endif
%ifarch x86_64
/usr/bin/i386
/usr/bin/x86_64
%endif
%dir /var/lib/hwclock

%files devel
%defattr(-,root,root)
/usr/include/blkid
/usr/include/libmount
/usr/include/uuid
/usr/%{_lib}/libblkid.la
/usr/%{_lib}/libmount.la
/usr/%{_lib}/libuuid.la
/usr/%{_lib}/libblkid.a
/usr/%{_lib}/libblkid.so
/usr/%{_lib}/libuuid.a
/usr/%{_lib}/libuuid.so
/usr/%{_lib}/libmount.a
/usr/%{_lib}/libmount.so
/usr/%{_lib}/pkgconfig/mount.pc
/usr/%{_lib}/pkgconfig/blkid.pc
/usr/%{_lib}/pkgconfig/uuid.pc
/usr/share/man/man3/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-3
- Optimize for size 

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-2
- Use the Obsoletes tag to override util-linux-ng packages

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-1
- Package name changed to util-linux
- Upgrade to version 2.20

* Thu Apr 28 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.18-2
- Fix hwclock to use /var/lib/hwclock/adjtime

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.18-1
- Upgrade to 2.18

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.17.2-1
- Upgrade to 2.17.2

* Mon Dec 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.16.2-1
- Upgrade to 2.16.2

* Sun Jul 26 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.16-1
- Initial version
