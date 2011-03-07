Summary: LightCube OS Build Essential Meta-Package
Name: build-essential
Version: 0.2
Release: 1
Group: Development/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: binutils
Requires: glibc-devel
Requires: linux-headers
Requires: gcc-c++
Requires: make
Requires: pkg-config
Requires: patch
Requires: bison
Requires: rpm-build

%description
A metapackage which provides no files itself, but ensures that all core
build essentials are installed.

%install

%files

%changelog
* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.2-1
- Add rpm-build dependency

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Initial version
