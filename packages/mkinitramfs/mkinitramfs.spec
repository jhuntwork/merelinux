Summary: mkinitramfs
Name: mkinitramfs
Version: 0.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lightcubeos
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, bash, cpio
BuildRequires: digest(sha1:%{SOURCE0}) = 7cbc1d658d28589d07b9b13e19ed0951149f39c9

%description
A simple script to generate an initramfs file for a specified kernel.

%prep
%setup -q

%build

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/mkinitramfs
/usr/share/mkinitramfs

%changelog
* Mon Sep 13 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.2-1
- Upgrade to 0.2 - add support for software raid

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Initial version
