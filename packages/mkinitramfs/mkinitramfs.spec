Summary: mkinitramfs
Name: mkinitramfs
Version: 0.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://dev.lightcube.us/projects/lightcubeos
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, bash, cpio
BuildRequires: digest(%{SOURCE0}) = 51ef84ed3750b639b94d3c1ee2a77a55

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
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Initial version
