Summary: libpng
Name: libpng
Version: 1.4.3
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.libpng.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.xz

Requires: base-layout, glibc, zlib
BuildRequires: digest(%{SOURCE0}) = 322e2e0c0dea7a374ce6e60d9a72e604
BuildRequires: zlib-devel

%description
libpng is the official PNG reference library. It supports almost all PNG
features, is extensible, and has been extensively tested for over 15 years

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libpng14.so.14
/usr/%{_lib}/libpng14.so.14.3.0

%files devel
%defattr(-,root,root)
/usr/bin/libpng-config
/usr/bin/libpng14-config
/usr/include/libpng14
/usr/include/png.h
/usr/include/pngconf.h
/usr/%{_lib}/libpng.a
/usr/%{_lib}/libpng.la
/usr/%{_lib}/libpng.so
/usr/%{_lib}/libpng14.a
/usr/%{_lib}/libpng14.la
/usr/%{_lib}/libpng14.so
/usr/%{_lib}/pkgconfig/libpng.pc
/usr/%{_lib}/pkgconfig/libpng14.pc
/usr/share/man/man3/libpng.3
/usr/share/man/man3/libpngpf.3
/usr/share/man/man5/png.5

%changelog
* Thu Aug 19 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.3-1
- Initial version
