Summary: LightCube OS Base System Meta-Package
Name: base-system
Version: 0.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: base-layout
Requires: coreutils
Requires: dhcp
Requires: diffutils
Requires: e2fsprogs
Requires: fcron
Requires: findutils
Requires: gawk
Requires: grep
Requires: grub
Requires: gettext
Requires: gzip
Requires: inetutils
Requires: iproute2
Requires: iputils
Requires: kbd
Requires: linux
Requires: less
Requires: logrotate
Requires: lsb-bootscripts
Requires: man-db
Requires: man-pages
Requires: mkinitramfs
Requires: module-init-tools
Requires: net-tools
Requires: ntp
Requires: openssh
Requires: parted
Requires: pciutils
Requires: procps
Requires: psmisc
Requires: rpm
Requires: rsync
Requires: screen
Requires: sed
Requires: shadow
Requires: smart
Requires: sysklogd
Requires: sysvinit
Requires: tar
Requires: sudo
Requires: udev
Requires: vim
Requires: wget
Requires: which
Requires: xfsprogs

%description
A metapackage which provides no files itself, but ensures that all base
packages are installed.

%install

%files

%changelog
* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.2-1
- Remove base-files and iana-etc, covered by base-layout

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-4
- Add iputils as a requirement

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-3
- Add net-tools as a requirement

* Fri Sep 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-2
- Add linux, grub and dhcp as requirements

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Initial version
