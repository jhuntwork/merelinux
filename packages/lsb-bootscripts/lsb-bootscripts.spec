Summary: LSB Bootscripts
Name: lsb-bootscripts
Version: 4.1.2
Release: 2
Group: System Environment/Base
License: MIT
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lsb-bootscripts
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 38a771fc7332bcfb9adfe3b0e59090c78da9d3f3

%description
LSB compatible bootscripts adapted from the LFS project.

%prep
%setup -q

%install
make DESTDIR=%{buildroot} minimal

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install_initd checkfs
/usr/sbin/install_initd cleanfs
/usr/sbin/install_initd halt
/usr/sbin/install_initd console
/usr/sbin/install_initd localnet
/usr/sbin/install_initd modules
/usr/sbin/install_initd mountfs
/usr/sbin/install_initd mountvirtfs
/usr/sbin/install_initd network
/usr/sbin/install_initd random
/usr/sbin/install_initd reboot
/usr/sbin/install_initd sendsignals
/usr/sbin/install_initd setclock
/usr/sbin/install_initd sysklogd
/usr/sbin/install_initd swap
/usr/sbin/install_initd sysctl
/usr/sbin/install_initd udev
/usr/sbin/install_initd udev_retry

%files
%defattr(-,root,root)
%config /etc/inittab
%config /etc/default/rc.site
%config /etc/rc.local
%dir /etc/network
/etc/init.d
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
/lib/lsb/init-functions
/lib/network-services
/sbin/ifdown
/sbin/ifup
/sbin/service

%changelog
* Mon Aug 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.2-2
- Install setclock scripts symlinks on post

* Mon Aug 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.2-1
- Upgrade to version 4.1.2
- Fixes to setclock script

* Sat Aug 20 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.1-1
- Upgrade version to 4.1.1
- Fixes to install procedure
- Add /etc/rc.local

* Sat Aug 20 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-1
- Upgrade version to 4.1 (matches LSB version)
- Fix PATH setting in scripts to use /usr/bin and /usr/sbin

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
