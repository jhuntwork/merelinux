Summary: The MPFR Library
Name: mpfr
Version: 2.4.1
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mpfr.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, gmp

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: glibc-devel, texinfo, linux-headers, binutils, gcc, %{name}

%description
The MPFR library is a C library for multiple-precision floating-point
computations with correct rounding.

%description devel
Provides headers, object files and info pages for use in developing
applications using %{name}.

%prep
%setup -q

%build
./configure --prefix=/usr --enable-thread-safe --libdir=/usr/%{_lib}
make
make check
make html

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info %{_infodir}/mpfr.info %{_infodir}/dir

%preun devel
/usr/bin/install-info --delete %{_infodir}/mpfr.info %{_infodir}/dir

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
%doc mpfr.html/*.html

%changelog
* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
