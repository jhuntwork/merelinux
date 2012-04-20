Summary: mkinitramfs
Name: mkinitramfs
Version: 0.5.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lightcubeos
Source0: Makefile.mkinitramfs
Source1: init.in
Source2: initcd.in
Source3: mkinitramfs.orig

BuildRequires: digest(sha1:%{SOURCE0}) = eed5ec665723af5a38203ca13da017109d6ab092
BuildRequires: digest(sha1:%{SOURCE1}) = 3e6e9618dc9bdd7f2aa9c09d8f8483c6cc9eef16
BuildRequires: digest(sha1:%{SOURCE2}) = 7574764e55381f01048408141659201e7b1ddc24
BuildRequires: digest(sha1:%{SOURCE3}) = c1e163b35b910489ef0c05881e56b84e08710ee9

Requires: base-layout
Requires: bash
Requires: busybox
Requires: cpio
Requires: udev

%description
A simple script to generate an initramfs file for a specified kernel.

%prep
%setup -T -c
cp %{SOURCE0} %{SOURCE1} %{SOURCE2} %{SOURCE3} .

%build

%install
make -f %{SOURCE0} DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/mkinitramfs
/usr/share/mkinitramfs

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.5.2-1
- Initial version
