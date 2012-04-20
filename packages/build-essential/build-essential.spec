Summary: LightCube OS Build Essential Meta-Package
Name: build-essential
Version: 1.0
Release: 1
Group: Development/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: binutils
Requires: musl-devel
Requires: linux-headers
Requires: gcc
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
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0-1
- Initial version
