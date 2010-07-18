Summary: The MPC Library
Name: mpc
Version: 0.8.2
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.multiprecision.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, gmp, mpfr
BuildRequires: digest(%{SOURCE0}) = e98267ebd5648a39f881d66797122fb6
BuildRequires: gmp-devel, mpfr-devel

%description
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result.

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: %{name}
Requires(post): texinfo, bash, ncurses, readline

%description devel
Provides headers, object files and info pages for use in developing
applications using %{name}.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info /usr/share/info/mpc.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/mpc.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/%{_lib}/libmpc.so.2
/usr/%{_lib}/libmpc.so.2.0.0

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libmpc.a
/usr/%{_lib}/libmpc.la
/usr/%{_lib}/libmpc.so
/usr/share/info/mpc.info
/usr/include/mpc.h

%changelog
* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.8.2-1
- Initial version
