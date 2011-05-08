Summary: The MPFR Library
Name: mpfr
Version: 3.0.1
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mpfr.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = fbf402fc196724ae60ef01eb6ca8490b1ea4db69
BuildRequires: gmp-devel

%description
The MPFR library is a C library for multiple-precision floating-point
computations with correct rounding.

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Provides headers, object files and info pages for use in developing
applications using %{name}.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --enable-thread-safe \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info /usr/share/info/mpfr.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/mpfr.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/%{_lib}/libmpfr.so.*

%files devel
%defattr(-,root,root)
/usr/include/mpf2mpfr.h
/usr/include/mpfr.h
/usr/%{_lib}/libmpfr.so
/usr/%{_lib}/libmpfr.a
/usr/%{_lib}/libmpfr.la
/usr/share/info/mpfr.info
/usr/share/doc/mpfr

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.1-1
- Upgrade to 3.0.1

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.0-1
- Upgrade to 3.0.0

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4.2-1
- Upgrade to 2.4.2

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
