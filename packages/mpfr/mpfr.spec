Summary: The MPFR Library
Name: mpfr
Version: 2.4.2
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mpfr.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, gmp
BuildRequires: digest(%{SOURCE0}) = 89e59fe665e2b3ad44a6789f40b059a0

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: %{name}
Requires(post): texinfo, bash, ncurses, readline

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
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4.2-1
- Upgrade to 2.4.2

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
