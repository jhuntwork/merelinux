Summary: LFS LSB Bootscripts
Name: lsb-bootscripts
Version: 3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.linuxfromscratch.org/lfs
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/lsb-v%{version}.tar.bz2
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/service

BuildRequires: digest(%{SOURCE0}) = 00a17787d60658868588aeb44ff51606
BuildRequires: digest(%{SOURCE1}) = dcf1319b248dd0f47f40cc0207c031bd

%description
LSB compatible bootscripts from the LFS project.

%prep
%setup -q -n lsb-v%{version}

%install
# Fix syntax error
sed -i 's@\]@& ; then@' init.d/sendsignals
# LightCube specifics
sed -i -e 's@Linux From Scratch@LightCube OS@g' \
  -e 's/lfs-dev@linuxfromscratch.org/support@lightcube.us/' \
  -e 's/DISTRO_MINI=.*/DISTRO_MINI="lightcube"/' \
  -e 's@lfs-functions@lightcube-functions@' sysconfig/rc.site
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/usr/sbin
install -m 754 %{SOURCE1} %{buildroot}/usr/sbin/service
mv -v %{buildroot}/etc/init.d/{lfs,lightcube}-functions

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/init.d
/etc/inittab
/etc/lsb
%dir /etc/rc0.d
%dir /etc/rc1.d
%dir /etc/rc2.d
%dir /etc/rc3.d
%dir /etc/rc4.d
%dir /etc/rc5.d
%dir /etc/rc6.d
%dir /etc/rcS.d
/etc/rc0.d/K94network
/etc/rc0.d/K95sysklogd
/etc/rc0.d/K96sendsignals
/etc/rc0.d/K97mountfs
/etc/rc0.d/K98swap
/etc/rc0.d/K99localnet
/etc/rc0.d/S00halt
/etc/rc1.d/K98network
/etc/rc1.d/K99sysklogd
/etc/rc2.d/K99network
/etc/rc2.d/S00sysklogd
/etc/rc3.d/S00sysklogd
/etc/rc3.d/S01network
/etc/rc4.d/S00sysklogd
/etc/rc4.d/S01network
/etc/rc5.d/S00sysklogd
/etc/rc5.d/S01network
/etc/rc6.d/K94network
/etc/rc6.d/K95sysklogd
/etc/rc6.d/K96sendsignals
/etc/rc6.d/K97mountfs
/etc/rc6.d/K98swap
/etc/rc6.d/K99localnet
/etc/rc6.d/S00reboot
/etc/rcS.d/S00mountkernfs
/etc/rcS.d/S01sysctl
/etc/rcS.d/S02modules
/etc/rcS.d/S03udev
/etc/rcS.d/S04swap
/etc/rcS.d/S05setclock
/etc/rcS.d/S06checkfs
/etc/rcS.d/S07mountfs
/etc/rcS.d/S08udev_retry
/etc/rcS.d/S09localnet
/etc/rcS.d/S10console
/etc/rcS.d/S11cleanfs
/etc/sysconfig/createfiles
/etc/sysconfig/modules
/etc/sysconfig/network-devices
/etc/sysconfig/rc
/etc/sysconfig/rc.site
/lib/lsb/init-functions
/lib/lsb/manage-functions
/usr/sbin/service

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3-1
- Initial version
