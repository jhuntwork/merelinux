Summary: The MPC Library
Name: mpc
Version: 0.9
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.multiprecision.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 229722d553030734d49731844abfef7617b64f1a
BuildRequires: gmp-devel
BuildRequires: mpfr-devel

%description
Mpc is a C library for the arithmetic of complex numbers with arbitrarily
high precision and correct rounding of the result.

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
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.9-1
- Upgrade to 0.9

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.8.2-1
- Initial version
