Summary: Util-Linux Next Generation
Name: util-linux-libs
Version: 2.20
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/util-linux
Source0: http://dev.lightcube.us/sources/util-linux/util-linux-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = e8cd2c8e968cdbdc097d82cceaf15d536e0254c1
BuildRequires: ncurses-devel
BuildRequires: zlib-devel

%description
Provides libblkid and libuuid

%package devel
Summary: %{name} headers and libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for libblkid and libuuid

%prep
%setup -q -n util-linux-%{version}
%{config_musl}
sed -i 's@etc/adjtime@var/lib/hwclock/adjtime@g' $(grep -rl '/etc/adjtime' .)

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe -fPIC'
./configure \
  --libdir=/lib
make V=1 -C libuuid %{PMFLAGS}
make V=1 -C libblkid %{PMFLAGS}

%install
make -C libuuid DESTDIR=%{buildroot} install
make -C libblkid DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/info
rm -f %{buildroot}/usr/lib/*.so
ln -s /lib/libuuid.so.1.3.0 %{buildroot}/usr/lib/libuuid.so
ln -s /lib/libblkid.so.1.1.0 %{buildroot}/usr/lib/libblkid.so
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/lib/libblkid.so.*
/lib/libuuid.so.*

%files devel
%defattr(-,root,root)
/usr/include/blkid
/usr/include/uuid
/usr/lib/libblkid.la
/usr/lib/libuuid.la
/usr/lib/libblkid.a
/usr/lib/libblkid.so
/usr/lib/libuuid.a
/usr/lib/libuuid.so
/usr/lib/pkgconfig/blkid.pc
/usr/lib/pkgconfig/uuid.pc
/usr/share/man/man3/*.bz2

%changelog
* Mon Feb 06 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-1
- Initial version
