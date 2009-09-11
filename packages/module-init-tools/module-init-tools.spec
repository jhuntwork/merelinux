Summary: module-init-tools
Name: module-init-tools
Version: 3.10
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, zlib

%description
Tools for activating Linux kernel modules

%prep
%setup -q

%build
./configure --prefix=/ --enable-zlib --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} INSTALL=install install
rm -f %{buildroot}/usr/info/dir

%post
/usr/bin/install-info %{_infodir}/diff.info %{_infodir}/dir

%preun
/usr/bin/install-info --delete %{_infodir}/diff.info %{_infodir}/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/lsmod
/sbin/depmod
/sbin/insmod
/sbin/insmod.static
/sbin/modinfo
/sbin/modprobe
/sbin/rmmod
/usr/share/man/man5/depmod.conf.5
/usr/share/man/man5/modprobe.conf.5
/usr/share/man/man5/modprobe.d.5
/usr/share/man/man5/modules.dep.5
/usr/share/man/man8/depmod.8
/usr/share/man/man8/insmod.8
/usr/share/man/man8/lsmod.8
/usr/share/man/man8/modinfo.8
/usr/share/man/man8/modprobe.8
/usr/share/man/man8/rmmod.8

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
