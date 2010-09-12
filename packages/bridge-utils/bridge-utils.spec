Summary: Bridge Utilities
Name: bridge-utils
Version: 1.4
Release: 1
Group: System Environment/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.linuxfoundation.org/collaborate/workgroups/networking/bridge
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 150a376f2463ae7e45164f3ffc63fd7d6f099c76
BuildRequires: autoconf

%description
Bridge utils provide utilities for creating and managing Ethernet bridges in
Linux

%package devel
Summary: Headers for developing with bridge-utils
Group: Development/Libraries
Requires: %{name}

%description devel
Headers for developing with bridge-utils

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
autoconf
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
bzip2 -9 %{buildroot}/usr/share/man/man8/brctl.8

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/sbin/brctl
/usr/share/man/man8/brctl.8.bz2

%files devel
/usr/include/libbridge.h
/usr/%{_lib}/libbridge.a

%changelog
* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4-1
- Initial version
