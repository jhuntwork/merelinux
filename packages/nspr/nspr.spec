Summary: NSPR
Name: nspr
Version: 4.8.7
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://developer.mozilla.org/En/NSPR
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 34d9eb75b47a3d19b57ef1ed5aef2004e79b5fc4

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
export LDFLAGS=%{LDFLAGS}
./configure \
  --prefix=/usr \
  --disable-debug \
  --enable-optimize \
  --libdir=/usr/%{_lib} %{_extra_args}
make %{PMFLAGS}

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
* Mon Apr 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.8.7-1
- Upgrade to 4.8.7

* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.8.6-1
- Initial version
