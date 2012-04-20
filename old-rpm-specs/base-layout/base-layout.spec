Summary: Base directory layout
Name: base-layout
Version: 1.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
Source0: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/passwd
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/group
Source2: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/inputrc
Source3: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/protocols
Source4: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/services

BuildRequires: digest(sha1:%{SOURCE0}) = ad00fdd5d578743a617f1cc9bb4eee4e25da3038
BuildRequires: digest(sha1:%{SOURCE1}) = 5b9663e555e16a3d671df05c537e51f7b9910ace
BuildRequires: digest(sha1:%{SOURCE2}) = b5b083ef90b918b68c67b7c54f37c91e46b5b706
BuildRequires: digest(sha1:%{SOURCE3}) = a6546de3329331caf3b43a726dde6cdc6951a28a
BuildRequires: digest(sha1:%{SOURCE4}) = 9153e46648c575b2c5a7ed69346d8ac42255c1d0
Provides: /

%description
Provides an empty filesystem layout with all necessary
directories for a standard system as well as a few base system files

%prep
%setup -T -c

%install
# Top-level directories
install -dv %{buildroot}/bin
install -dv %{buildroot}/boot
install -dv %{buildroot}/dev
install -dv %{buildroot}/etc/default
install -dv %{buildroot}/lib/lsb
install -dv %{buildroot}/home
install -dv %{buildroot}/include
install -dv %{buildroot}/lib/modules
install -dv %{buildroot}/media
install -dv %{buildroot}/media/floppy
install -dv %{buildroot}/media/cdrom
install -dv %{buildroot}/mnt
install -dv %{buildroot}/opt
install -dv %{buildroot}/proc
install -dv %{buildroot}/root
install -dv %{buildroot}/sbin
install -dv %{buildroot}/srv
install -dv %{buildroot}/sys
install -dv %{buildroot}/tmp
install -dv %{buildroot}/share/aclocal
install -dv %{buildroot}/share/dict
install -dv %{buildroot}/share/doc
install -dv %{buildroot}/share/info
install -dv %{buildroot}/share/locale
install -dv %{buildroot}/share/man
install -dv %{buildroot}/share/misc
install -dv %{buildroot}/share/terminfo
install -dv %{buildroot}/share/zoneinfo
install -dv %{buildroot}/src/kernels
install -dv %{buildroot}/var/cache
install -dv %{buildroot}/var/lock
install -dv %{buildroot}/var/lib/hwclock
install -dv %{buildroot}/var/lib/misc
install -dv %{buildroot}/var/lib/locate
install -dv %{buildroot}/var/log
install -dv %{buildroot}/var/mail
install -dv %{buildroot}/var/run
install -dv %{buildroot}/var/spool
install -dv %{buildroot}/var/tmp
install -dv %{buildroot}/var/spool/repackage
install -dv %{buildroot}/var/opt
install -m0644 %{SOURCE0} %{buildroot}/etc/passwd
install -m0644 %{SOURCE1} %{buildroot}/etc/group
install -m0644 %{SOURCE2} %{buildroot}/etc/inputrc
# The following two files were generated from the iana-etc package
# located at http://sethwklein.net/iana-etc
install -m0644 %{SOURCE3} %{buildroot}/etc/protocols
install -m0644 %{SOURCE4} %{buildroot}/etc/services

> %{name}.man
for man in man1 man2 man3 man4 man5 man6 man7 man8 man9 ; do
  mkdir -p %{buildroot}/share/man/$man
  echo "%dir %ghost /share/man/$man" >> %{name}.man
done

%clean
rm -rf %{buildroot}

%files -f %{name}.man
%defattr(-,root,root)
%dir /
%dir /bin
%dir /boot
%dir /dev
%dir /etc
%config(noreplace) /etc/passwd
%config(noreplace) /etc/group
%config /etc/inputrc
%config /etc/protocols
%config /etc/services
%dir /etc/default
%dir /home
%dir /lib
%dir /lib/lsb
%dir /lib/modules
%dir /media
%dir /media/floppy
%dir /media/cdrom
%dir /mnt
%dir /opt
%dir /proc
%attr(0750,root,root) %dir /root
%dir /sbin
%dir /srv
%dir /sys
%attr(1777,root,root) %dir /tmp
%dir /include
%dir /share
%dir /share/aclocal
%dir /share/dict
%dir /share/doc
%dir /share/info
%dir /share/locale
%dir /share/man
%dir /share/misc
%dir /share/terminfo
%dir /share/zoneinfo
%dir /src
%dir /src/kernels
%dir /var
%dir /var/cache
%dir /var/lib
%dir /var/lib/misc
%dir /var/lib/locate
%dir /var/lock
%dir /var/log
%dir /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%dir /var/spool/repackage
%attr(1777,root,root) %dir /var/tmp

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0-1
- Initial version
