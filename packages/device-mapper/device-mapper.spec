Summary: Device-mapper
Name: device-mapper
Version: 1.02.28
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sources.redhat.com/dm
Source: http://dev.lightcube.us/sources/%{name}/%{name}.%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = 0d1b4e27b5afa5f68b8bc6e1905f9430470045b7

%description
The Device-mapper is a component of the 2.6 linux kernel that supports logical
volume management.

%package devel
Summary: Headers and libraries for developing with libdevmapper
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with libdevmapper

%prep
%setup -q -n %{name}.%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libdevmapper.so.*
/usr/sbin/dmsetup
/usr/share/man/man8/dmsetup.8.bz2

%files devel
%defattr(-,root,root)
/usr/include/libdevmapper.h
/usr/lib64/libdevmapper.so

%changelog
* Thu Sep 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.02.28-1
- Initial version
