Summary: ext2, ext3 and ext4 File System Programs
Name: e2fsprogs
Version: 1.41.14
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://e2fsprogs.sourceforge.net
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 24f9364fa3d4c0d7d00cb627b819d0e51055d6c5
BuildRequires: util-linux-devel

%package devel
Summary: %{name} headers and libraries
Requires: %{name} >= %{version}

%description
%{name} provides core file system utilities associated with the
ext2, ext3 and ext4 filesystems

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
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
make %{PMFLAGS}
#make check

%install
cd build
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
gunzip %{buildroot}/usr/share/info/libext2fs.info.gz
makeinfo -o doc/com_err.info ../lib/et/com_err.texinfo
install -v -m644 doc/com_err.info %{buildroot}/usr/share/info
%{compress_man}
%{strip}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info /usr/share/info/libext2fs.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/com_err.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/libext2fs.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/com_err.info /usr/share/info/dir

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
/usr/%{_lib}/libcom_err.so.*
/usr/%{_lib}/libe2p.so.*
/usr/%{_lib}/libext2fs.so.*
/usr/%{_lib}/libss.so.*
/usr/sbin/filefrag
/usr/sbin/mklost+found
/usr/share/man/man1/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man8/*.bz2

%files devel
%defattr(-,root,root)
/usr/bin/mk_cmds
/usr/bin/compile_et
/usr/share/et
/usr/share/ss
/usr/share/info/libext2fs.info
/usr/share/info/com_err.info
/usr/share/man/man3/com_err.3.bz2
/usr/include/e2p
/usr/include/et
/usr/include/ext2fs
/usr/include/ss
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
* Thu Nov 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.14-2
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.14-1
- Upgrade to 1.41.14

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.12-1
- Upgrade to 1.41.12

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.11-1
- Upgrade to 1.41.11

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
