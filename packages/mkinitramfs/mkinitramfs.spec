Summary: mkinitramfs
Name: mkinitramfs
Version: 0.9.11
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/sed
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, libbash
BuildRequires: digest(%{SOURCE0}) = 2f2ca56f66cffdfe3738b5a80b1ad1df
BuildRequires: libbash

%description
mkinitramfs is intended to create the ultimate initramfs image. It's designed to
boot from any media (SATA,PATA,SCSI,USB,even CDROM...) without any changes
being made to your disk

%prep
%setup -q

%build
./configure --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
/usr/sbin/mkinitramfs
/usr/share/mkinitramfs

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.9.11-1
- Initial version
