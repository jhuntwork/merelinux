Summary: Util-Linux Next Generation
Name: util-linux-ng
Version: 2.17.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://userweb.kernel.org/~kzak/util-linux-ng
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 4635725a3eef1c57090bac8ea5e082e6

%package devel
Summary: %{name} headers and libraries
Requires: glibc-devel, linux-headers, binutils, gcc, %{name}

%description
%{name} provides some core Linux utilities

%description devel
Headers and libraries for libblkid and libuuid

%prep
%setup -q

%build
sed -i 's@etc/adjtime@var/%{_lib}/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)
./configure --enable-arch --enable-partx --enable-write --libdir=/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
rm -vf %{buildroot}/usr/share/info/dir
rm %{buildroot}/usr/share/getopt/*.tcsh
find %{buildroot} -name *.la -exec rm -v '{}' \;
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info %{_infodir}/ipc.info %{_infodir}/dir

%preun devel
/usr/bin/install-info --delete %{_infodir}/ipc.info %{_infodir}/dir

%files -f %{name}.lang
%defattr(-,root,root)
/bin/arch
/bin/dmesg
/bin/more
/bin/mount
/bin/umount
/sbin/agetty
/%{_lib}/libblkid.so.*
/%{_lib}/libuuid.so.*
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
/usr/bin/ddate
/usr/bin/fallocate
/usr/bin/flock
/usr/bin/getopt
/usr/bin/hexdump
/usr/bin/ionice
/usr/bin/ipcmk
/usr/bin/ipcrm
/usr/bin/ipcs
/usr/bin/isosize
/usr/bin/line
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
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*
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

%files devel
%defattr(-,root,root)
/usr/share/info/ipc.info
/usr/share/man/man3/*
/usr/include/blkid/blkid.h
/usr/include/uuid/uuid.h
/usr/%{_lib}/libblkid.a
/usr/%{_lib}/libblkid.so
/usr/%{_lib}/libuuid.a
/usr/%{_lib}/libuuid.so
/usr/%{_lib}/pkgconfig/blkid.pc
/usr/%{_lib}/pkgconfig/uuid.pc

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.17.2-1
- Upgrade to 2.17.2

* Mon Dec 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.16.2-1
- Upgrade to 2.16.2

* Sun Jul 26 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.16-1
- Initial version
