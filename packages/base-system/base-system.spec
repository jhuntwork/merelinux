Summary: LightCube OS Base System Meta-Package
Name: base-system
Version: 0.1
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: base-layout
Requires: base-files
Requires: linux
Requires: grub
Requires: procps
Requires: psmisc
Requires: pciutils
Requires: cpio
Requires: udev
Requires: bash
Requires: wget
Requires: which
Requires: sudo
Requires: screen
Requires: mkinitramfs
Requires: cpio
Requires: parted
Requires: coreutils
Requires: logrotate
Requires: sysklogd
Requires: sysvinit
Requires: iana-etc
Requires: man-db
Requires: man-pages
Requires: e2fsprogs
Requires: gettext
Requires: xfsprogs
Requires: grep
Requires: dhcp
Requires: fcron
Requires: gawk
Requires: diffutils
Requires: findutils
Requires: lsb-bootscripts
Requires: kbd
Requires: gzip
Requires: less
Requires: iproute2
Requires: inetutils
Requires: net-tools
Requires: tar
Requires: sed
Requires: ntp
Requires: shadow
Requires: rsync
Requires: openssh
Requires: module-init-tools
Requires: rpm
Requires: smart
Requires: vim

%description
A metapackage which provides no files itself, but ensures that all base
packages are installed.

%install

%files

%changelog
* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-3
- Add net-tools as a requirement

* Fri Sep 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-2
- Add linux, grub and dhcp as requirements

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Initial version
