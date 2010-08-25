Summary: initd-tools
Name: initd-tools
Version: 0.1.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.dwcab.com/projects/initd-tools
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = ab6377700ace81ec5a556ebdbae1d8d9

%description
initd-tools is an implementation of the init script installation and removal
programs in Linux Standard Base (LSB) 3.2 specification.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure
make
make check

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/lsb/install_initd
/usr/lib/lsb/remove_initd
/usr/sbin/install_initd
/usr/sbin/remove_initd
/usr/share/man/man8/install_initd.8
/usr/share/man/man8/remove_initd.8

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1.3-1
- Initial version
