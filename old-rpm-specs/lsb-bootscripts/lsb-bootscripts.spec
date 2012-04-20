Summary: LSB Bootscripts
Name: lsb-bootscripts
Version: 4.2.0
Release: 1
Group: System Environment/Base
License: MIT
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lsb-bootscripts
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 3cd9e3efaa0d55b7ff0337cf7642be3d570a9fbc

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
* Thu Jan 31 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.0-1
- Initial version
