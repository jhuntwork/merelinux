Summary: GRand Unified Bootloader
Name: grub
Version: 1.98
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/grub
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = e83a2c438f4773a2e272c225983c0145e1ffd641

%description
GNU GRUB is a Multiboot boot loader. It is responsible for loading and
transferring control to the operating system kernel software

%prep
%setup -q
%{config_musl}
mv po/ OLD-po/
sed -i 's@loff_t@off_t@g' util/hostdisk.c
sed -i -e '402 s@linux@musl@' util/hostdisk.c

%build
export CFLAGS="-D_GNU_SOURCE -Os -pipe"
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --disable-werror \
  --disable-grub-emu-usb \
  --disable-grub-fstest \
  --disable-efiemu
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
for file in `grep -r -l '\-qx' %{buildroot}`
do
    sed -i 's@-qx@-q@' $file
done
for file in `grep -r -l '\-vx' %{buildroot}` 
do
    sed -i 's@-vx@-q@' $file
done


%clean
rm -rf %{buildroot}

%files
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
/usr/lib/grub
/usr/sbin/grub-install
/usr/sbin/grub-mkconfig
/usr/sbin/grub-mkdevicemap
/usr/sbin/grub-probe
/usr/sbin/grub-reboot
/usr/sbin/grub-set-default
/usr/sbin/grub-setup

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.98-1
- Initial version
