Summary: popt
Name: popt
Version: 1.16
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://rpm5.org/files/popt
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 3743beefa3dd6247a73f8f7a32c14c33

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
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
%if %{_lib} != "lib"
mv %{buildroot}/usr/lib/pkgconfig %{buildroot}/usr/%{_lib}/
%endif
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
/usr/%{_lib}/pkgconfig/popt.pc
/usr/share/man/man3/popt.3


%changelog
* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.16-1
- Upgrade to 1.16

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.15-1
- Initial version
