Summary: LSB Bootscripts
Name: lsb-bootscripts
Version: 4.0
Release: 1
Group: System Environment/Base
License: MIT
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lsb-bootscripts
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 9569a5023dc159aab8d4c6c5589e928bd43d3e87

%description
LSB compatible bootscripts adapted from the LFS project.

%prep
%setup -q

%install
make ETCDIR=/etc DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/init.d
%dir /etc/network
%config /etc/inittab
/etc/rc0.d
/etc/rc1.d
/etc/rc2.d
/etc/rc3.d
/etc/rc4.d
/etc/rc5.d
/etc/rc6.d
/etc/rcS.d
/etc/default/createfiles
/etc/default/modules
/etc/default/rc
%config /etc/default/rc.site
/lib/lsb/init-functions
/lib/network-services
/sbin/ifdown
/sbin/ifup
/sbin/service

%changelog
* Sat Aug 20 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-1
- Fork from LFS project.
- New directory layout.
- New version: 4.0

* Sat Sep 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3-4
- Add random seed handling

* Fri Sep 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3-3
- Add dhclient service

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3-2
- Fix quotes in service script

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3-1
- Initial version
