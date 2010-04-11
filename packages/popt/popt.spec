Summary: popt
Name: popt
Version: 1.15
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://rpm5.org/files/popt
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = c61ef795fa450eb692602a661ec8d7f1

%description
The popt library exists essentially for parsing command line options.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/usr/%{_lib}/libpopt.so.*

%files devel
%defattr(-,root,root)
/usr/include/popt.h
/usr/%{_lib}/libpopt.a
/usr/%{_lib}/libpopt.la
/usr/%{_lib}/libpopt.so
/usr/share/man/man3/popt.3


%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.15-1
- Initial version
