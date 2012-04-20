Summary: LightCube OS Base System Meta-Package
Name: base-system
Version: 0.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: base-layout
#Requires: dhcp
Requires: fcron
#Requires: grub
Requires: linux
#Requires: logrotate
Requires: lsb-bootscripts
Requires: mkinitramfs
Requires: openssh
Requires: rpm
Requires: rsync
Requires: smart
Requires: sudo
Requires: udev
Requires: wget

%description
A metapackage which provides no files itself, but ensures that all base
packages are installed.

%install

%files

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.3-1
- Initial version
