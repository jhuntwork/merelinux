Summary: GRand Unified Bootloader
Name: grub
Version: 1.98
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/grub
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = c0bcf60e524739bb64e3a2d4e3732a59
Requires(post): texinfo, bash, ncurses, readline

%description
GNU GRUB is a Multiboot boot loader. It is responsible for loading and
transferring control to the operating system kernel software

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --libdir=/usr/%{_lib} \
  --disable-grub-emu-usb \
  --disable-grub-fstest \
  --disable-efiemu
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/grub.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/grub.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/etc/grub.d
/usr/bin/grub-bin2h
/usr/bin/grub-editenv
/usr/bin/grub-mkelfimage
/usr/bin/grub-mkimage
/usr/bin/grub-mkisofs
/usr/bin/grub-mkpasswd-pbkdf2
/usr/bin/grub-mkrelpath
/usr/bin/grub-mkrescue
/usr/bin/grub-script-check
/usr/%{_lib}/grub
/usr/sbin/grub-install
/usr/sbin/grub-mkconfig
/usr/sbin/grub-mkdevicemap
/usr/sbin/grub-probe
/usr/sbin/grub-reboot
/usr/sbin/grub-set-default
/usr/sbin/grub-setup
/usr/share/info/grub.info

%changelog
* Sat Apr 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.98-1
- Initial version
