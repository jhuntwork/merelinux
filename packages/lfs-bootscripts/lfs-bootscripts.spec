Summary: LFS Bootscripts
Name: lfs-bootscripts
Version: 20100124
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.linuxfromscratch.org/lfs
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, sysvinit, bash, util-linux-ng, coreutils, udev
BuildRequires: digest(%{SOURCE0}) = 4e832c2fea0afa8a536ea2247b425bd9

%description
Simple initial bootscripts from the LFS project.

%prep
%setup -q

%install
make DESTDIR=%{buildroot} install
ln -sv rc.d/init.d %{buildroot}/etc/init.d

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/init.d
%dir /etc/rc.d
%dir /etc/rc.d/init.d
%dir /etc/rc.d/rc0.d
%dir /etc/rc.d/rc1.d
%dir /etc/rc.d/rc2.d
%dir /etc/rc.d/rc3.d
%dir /etc/rc.d/rc4.d
%dir /etc/rc.d/rc5.d
%dir /etc/rc.d/rc6.d
%dir /etc/rc.d/rcsysinit.d
%dir /etc/sysconfig
%dir /etc/sysconfig/network-devices
%dir /etc/sysconfig/network-devices/services
/etc/rc.d/init.d/checkfs
/etc/rc.d/init.d/cleanfs
/etc/rc.d/init.d/console
/etc/rc.d/init.d/consolelog
/etc/rc.d/init.d/functions
/etc/rc.d/init.d/halt
/etc/rc.d/init.d/localnet
/etc/rc.d/init.d/modules
/etc/rc.d/init.d/mountfs
/etc/rc.d/init.d/mountkernfs
/etc/rc.d/init.d/network
/etc/rc.d/init.d/rc
/etc/rc.d/init.d/reboot
/etc/rc.d/init.d/sendsignals
/etc/rc.d/init.d/setclock
/etc/rc.d/init.d/swap
/etc/rc.d/init.d/sysctl
/etc/rc.d/init.d/sysklogd
/etc/rc.d/init.d/template
/etc/rc.d/init.d/udev
/etc/rc.d/init.d/udev_retry
/etc/rc.d/rc0.d/K80network
/etc/rc.d/rc0.d/K90sysklogd
/etc/rc.d/rc0.d/S60sendsignals
/etc/rc.d/rc0.d/S70mountfs
/etc/rc.d/rc0.d/S80swap
/etc/rc.d/rc0.d/S90localnet
/etc/rc.d/rc0.d/S99halt
/etc/rc.d/rc1.d/K80network
/etc/rc.d/rc1.d/K90sysklogd
/etc/rc.d/rc2.d/K80network
/etc/rc.d/rc2.d/K90sysklogd
/etc/rc.d/rc3.d/S10sysklogd
/etc/rc.d/rc3.d/S20network
/etc/rc.d/rc4.d/S10sysklogd
/etc/rc.d/rc4.d/S20network
/etc/rc.d/rc5.d/S10sysklogd
/etc/rc.d/rc5.d/S20network
/etc/rc.d/rc6.d/K80network
/etc/rc.d/rc6.d/K90sysklogd
/etc/rc.d/rc6.d/S60sendsignals
/etc/rc.d/rc6.d/S70mountfs
/etc/rc.d/rc6.d/S80swap
/etc/rc.d/rc6.d/S90localnet
/etc/rc.d/rc6.d/S99reboot
/etc/rc.d/rcsysinit.d/S00mountkernfs
/etc/rc.d/rcsysinit.d/S02consolelog
/etc/rc.d/rcsysinit.d/S05modules
/etc/rc.d/rcsysinit.d/S10udev
/etc/rc.d/rcsysinit.d/S20swap
/etc/rc.d/rcsysinit.d/S30checkfs
/etc/rc.d/rcsysinit.d/S40mountfs
/etc/rc.d/rcsysinit.d/S45cleanfs
/etc/rc.d/rcsysinit.d/S50udev_retry
/etc/rc.d/rcsysinit.d/S70console
/etc/rc.d/rcsysinit.d/S80localnet
/etc/rc.d/rcsysinit.d/S90sysctl
/etc/sysconfig/createfiles
/etc/sysconfig/modules
/etc/sysconfig/network-devices/ifdown
/etc/sysconfig/network-devices/ifup
/etc/sysconfig/network-devices/services/ipv4-static
/etc/sysconfig/network-devices/services/ipv4-static-route
/etc/sysconfig/rc

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20100124-1
- Initial version
