Summary: ext2, ext3 and ext4 File System Programs
Name: e2fsprogs
Version: 1.41.14
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://e2fsprogs.sourceforge.net
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 24f9364fa3d4c0d7d00cb627b819d0e51055d6c5
BuildRequires: util-linux-libs-devel

%package devel
Summary: %{name} headers and libraries
Requires: %{name} >= %{version}

%description
%{name} provides core file system utilities associated with the
ext2, ext3 and ext4 filesystems

%description devel
Headers and libraries for developing with %{name}

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}
sed -i 's@open64@open@g' misc/mke2fs.c
sed -i 's@lseek64@lseek@g' lib/ext2fs/llseek.c lib/blkid/llseek.c misc/e2image.c 
sed -i '/sys\/signal\.h/d' misc/fsck.c

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe -Werror=implicit-function-declaration -DHAVE_LSEEK64 -DHAVE_LSEEK64_PROTOTYPE'
mkdir build
cd build
../configure \
  --prefix=/usr \
  --with-root-prefix="" \
  --enable-elf-shlibs \
  --disable-libblkid \
  --disable-libuuid \
  --disable-uuidd \
  --disable-tls
make V=1 %{PMFLAGS}
#make check

%install
cd build
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-libs
rm -rf %{buildroot}/usr/share/locale
rm -rf %{buildroot}/usr/lib/charset.alias
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/mke2fs.conf
/lib/libcom_err.so.*
/lib/libe2p.so.*
/lib/libext2fs.so.*
/lib/libss.so.*
/sbin/badblocks
/sbin/debugfs
/sbin/dumpe2fs
/sbin/e2fsck
/sbin/e2image
/sbin/e2label
/sbin/e2undo
/sbin/fsck
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
/usr/lib/e2initrd_helper
/usr/sbin/filefrag
/usr/sbin/mklost+found

%files devel
%defattr(-,root,root)
/usr/bin/mk_cmds
/usr/bin/compile_et
/usr/include/e2p
/usr/include/et
/usr/include/ext2fs
/usr/include/ss
/usr/lib/libcom_err.a
/usr/lib/libcom_err.so
/usr/lib/libe2p.a
/usr/lib/libe2p.so
/usr/lib/libext2fs.a
/usr/lib/libext2fs.so
/usr/lib/libss.a
/usr/lib/libss.so
/usr/lib/pkgconfig/com_err.pc
/usr/lib/pkgconfig/e2p.pc
/usr/lib/pkgconfig/ext2fs.pc
/usr/lib/pkgconfig/ss.pc

%files extras
/usr/share/et
/usr/share/ss
/usr/share/man/man1/*.bz2
/usr/share/man/man3/*.bz2
/usr/share/man/man5/*.bz2 
/usr/share/man/man8/*.bz2

%changelog
* Sat Feb 04 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.41.11-1
- Initial version
