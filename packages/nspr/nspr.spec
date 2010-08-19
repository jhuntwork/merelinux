Summary: NSPR
Name: nspr
Version: 4.8.6
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://developer.mozilla.org/en/NSPR
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 592c275728c29d193fdba8009165990b

%description
Netscape Portable Runtime (NSPR) provides a platform-neutral API for system
level and libc-like functions. The API is used in the Mozilla clients, many
of Red Hat's and Sun's server applications, and other software offerings.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%ifarch x86_64
%define _extra_args --enable-64bit
%endif

%prep
%setup -q

%build
cd mozilla/nsprpub
./configure \
  --prefix=/usr \
  --disable-debug \
  --enable-optimize \
  --libdir=/usr/%{_lib} %{_extra_args}
make

%install
cd mozilla/nsprpub
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libplc4.so
/usr/%{_lib}/libnspr4.so
/usr/%{_lib}/libplds4.so

%files devel
%defattr(-,root,root)
/usr/bin/compile-et.pl
/usr/bin/prerr.properties
/usr/bin/nspr-config
/usr/%{_lib}/libnspr4.a
/usr/%{_lib}/libplc4.a
/usr/%{_lib}/libplds4.a
/usr/include/nspr
/usr/share/aclocal/nspr.m4

%changelog
* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.8.6-1
- Initial version
