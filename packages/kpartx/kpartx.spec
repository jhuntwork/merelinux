Summary: kpartx
Name: kpartx
Version: 0.4.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://christophe.varoqui.free.fr
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
# Source package extracted from the multipath-tools archive
BuildRequires: digest(sha1:%{SOURCE0}) = 573fa7af5eab3d4decd59b063e485981912bf854
BuildRequires: LVM2-libdevmapper-devel

%description
A tool for creating device maps from partition tables

%prep
%setup -q

%build
make LDFLAGS="%{LDFLAGS} -ldevmapper"

%install
make DESTDIR=%{buildroot} install
gunzip %{buildroot}/usr/share/man/man8/kpartx.8.gz
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/sbin/kpartx
/etc/udev/rules.d/kpartx.rules
/lib/udev/kpartx_id
/usr/share/man/man8/kpartx.8.bz2

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.4.9-1
- Initial version
