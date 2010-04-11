Summary: The GNU Multiple Precision Arithmetic Library
Name: gmp
Version: 5.0.1
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://gmplib.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 6bac6df75c192a13419dfd71d19240a7

%ifarch x86_64
%define my_build "--build=x86_64-unknown-linux-gnu"
%endif

%ifarch i686
%define my_build "--build=i686-pc-linux-gnu"
%endif

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: %{name}
Requires(post): texinfo, bash, ncurses, readline

%description
GMP is a free library for arbitrary precision arithmetic,
operating on signed integers, rational numbers, and floating
point numbers.

%description devel
Provides headers, object files and info pages for use in developing
applications using %{name}.

%prep
%setup -q

%build
./configure --prefix=/usr --enable-cxx --enable-mpbsd --libdir=/usr/%{_lib} %{my_build}
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post devel
/usr/bin/install-info %{_infodir}/gmp.info %{_infodir}/dir

%preun devel
/usr/bin/install-info --delete %{_infodir}/gmp.info %{_infodir}/dir

%files
%defattr(-,root,root)
/usr/%{_lib}/libgmp.so.*
/usr/%{_lib}/libmp.so.*
/usr/%{_lib}/libgmpxx.so.*

%files devel
%defattr(-,root,root)
/usr/include/gmp.h
/usr/include/gmpxx.h
/usr/include/mp.h
/usr/%{_lib}/libgmp*a
/usr/%{_lib}/libmp*a
/usr/%{_lib}/libgmp.so
/usr/%{_lib}/libmp.so
/usr/%{_lib}/libgmpxx.so
/usr/share/info/gmp.info
/usr/share/info/gmp.info-1
/usr/share/info/gmp.info-2

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.0.1-1
- Upgrade to 5.0.1

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
