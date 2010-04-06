Summary: ext2, ext3 and ext4 File System Programs
Name: e2fsprogs
Version: 1.41.11
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://e2fsprogs.sourceforge.net
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, util-linux-ng
BuildRequires: digest(%{SOURCE0}) = fb507a40c2706bc38306f150d069e345

%package devel
Summary: %{name} headers and libraries
Requires: glibc-devel, linux-headers, binutils, gcc, %{name}, pkgconfig

%description
%{name} provides core file system utilities associated with the
ext2, ext3 and ext4 filesystems

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
mkdir -v build
cd build
../configure \
  --prefix=/usr \
  --with-root-prefix="" \
  --enable-elf-shlibs \
  --libdir=/usr/%{_lib} \
  --disable-libblkid \
  --disable-libuuid \
  --disable-uuidd \
  --disable-fsck
make
make check

%install
cd build
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
gunzip %{buildroot}/usr/share/info/libext2fs.info.gz
makeinfo -o doc/com_err.info ../lib/et/com_err.texinfo
install -v -m644 doc/com_err.info %{buildroot}/usr/share/info
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info %{_infodir}/libext2fs.info %{_infodir}/dir
/usr/bin/install-info %{_infodir}/com_err.info %{_infodir}/dir

%preun devel
/usr/bin/install-info --delete %{_infodir}/libext2fs.info %{_infodir}/dir
/usr/bin/install-info --delete %{_infodir}/com_err.info %{_infodir}/dir

%files -f build/%{name}.lang
%defattr(-,root,root)
/etc/mke2fs.conf
/sbin/badblocks
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2image
/sbin/e2label
/sbin/e2undo
/sbin/fsck.ext2
/sbin/fsck.ext3
/sbin/fsck.ext4
/sbin/fsck.ext4dev
/sbin/logsave
/sbin/mke2fs
/sbin/mkfs.ext2
/sbin/mkfs.ext3
/sbin/mkfs.ext4
/sbin/mkfs.ext4dev
/sbin/resize2fs
/sbin/tune2fs
/usr/bin/chattr
/usr/bin/lsattr
/usr/sbin/e2freefrag
/usr/%{_lib}/e2initrd_helper
/usr/%{_lib}/libcom_err.so
/usr/%{_lib}/libcom_err.so.*
/usr/%{_lib}/libe2p.so.*
/usr/%{_lib}/libext2fs.so.*
/usr/%{_lib}/libss.so.*
/usr/sbin/filefrag
/usr/sbin/mklost+found
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/usr/bin/mk_cmds
/usr/bin/compile_et
/usr/share/et
/usr/share/ss
/usr/share/info/libext2fs.info
/usr/share/info/com_err.info
/usr/share/man/man3/com_err.3
/usr/include/e2p
/usr/include/et
/usr/include/ext2fs
/usr/include/ss
/usr/%{_lib}/e2initrd_helper
/usr/%{_lib}/libcom_err.a
/usr/%{_lib}/libcom_err.so
/usr/%{_lib}/libe2p.a
/usr/%{_lib}/libe2p.so
/usr/%{_lib}/libext2fs.a
/usr/%{_lib}/libext2fs.so
/usr/%{_lib}/libss.a
/usr/%{_lib}/libss.so
/usr/%{_lib}/pkgconfig/com_err.pc
/usr/%{_lib}/pkgconfig/e2p.pc
/usr/%{_lib}/pkgconfig/ext2fs.pc
/usr/%{_lib}/pkgconfig/ss.pc

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.11-1
- Upgrade to 1.41.11

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
