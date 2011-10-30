Summary: Base directory layout
Name: base-layout
Version: 0.4
Release: 1 
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Source0: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/lang-iso
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/lang-exceptions
Source2: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/passwd
Source3: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/group
Source4: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/inputrc
Source5: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/protocols
Source6: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/base-layout/services

BuildRequires: digest(sha1:%{SOURCE0}) = 9b091c035b2959b085ef7e46f242451bce844d4c
BuildRequires: digest(sha1:%{SOURCE1}) = 890e047e6b8a2a34f84f0214bbd4a6fcf7bd1d05
BuildRequires: digest(sha1:%{SOURCE2}) = ad00fdd5d578743a617f1cc9bb4eee4e25da3038
BuildRequires: digest(sha1:%{SOURCE3}) = 5b9663e555e16a3d671df05c537e51f7b9910ace
BuildRequires: digest(sha1:%{SOURCE4}) = b5b083ef90b918b68c67b7c54f37c91e46b5b706
BuildRequires: digest(sha1:%{SOURCE5}) = a6546de3329331caf3b43a726dde6cdc6951a28a
BuildRequires: digest(sha1:%{SOURCE6}) = 9153e46648c575b2c5a7ed69346d8ac42255c1d0
Obsoletes: base-files
Obsoletes: iana-etc
Provides: /
# Remove once base-files is gone from packages
Provides: base-files

%description
Provides an empty filesystem layout with all necessary
directories for a standard system as well as a few base system files

%prep
%setup -T -c

%install
# Top-level directories
install -dv %{buildroot}/{bin,boot,dev,etc/default,home,lib,media,mnt,opt,proc,root,sbin,srv,sys,tmp,usr,var}
install -dv %{buildroot}/lib/{lsb,modules}
install -dv %{buildroot}/media/{floppy,cdrom}
install -dv %{buildroot}/usr/{,local/}{bin,include,lib/lsb,sbin,src}
install -dv %{buildroot}/usr/src/kernels
install -dv %{buildroot}/usr/{,local/}share/{aclocal,dict,doc,info,locale}
install -dv %{buildroot}/usr/{,local/}share/{man,misc,terminfo,zoneinfo}
install -dv %{buildroot}/var/{lock,log,mail,run,spool,tmp}
install -dv %{buildroot}/var/spool/repackage
install -dv %{buildroot}/var/{opt,cache,lib/{hwclock,misc,locate},local}
install -m0644 %{SOURCE2} %{buildroot}/etc/passwd
install -m0644 %{SOURCE3} %{buildroot}/etc/group
install -m0644 %{SOURCE4} %{buildroot}/etc/inputrc
# The following two files were generated from the iana-etc package
# located at http://sethwklein.net/iana-etc
install -m0644 %{SOURCE5} %{buildroot}/etc/protocols
install -m0644 %{SOURCE6} %{buildroot}/etc/services

%ifarch ppc
install -dv %{buildroot}/usr/%{_lib}/nof
%endif

> %{name}.man
for man in man{{1..9}{,x},{0,1,3}p,n}; do
	mkdir -p %{buildroot}/usr/share/man/$man
	echo "%dir %ghost /usr/share/man/$man" >> %{name}.man
done
for loc in bg cs da de el en eo es fi fr fr.ISO8859-1 fr.UTF-8 \
  hr hu id it it.ISO8859-1 it.UTF-8 ja ko nl pl pl.ISO8859-2 pl.UTF-8 pt pt_BR \
  ro ru ru.UTF-8 ru.KOI8-R sk sl sv tr zh_CN zh_TW; do
	mkdir -p %{buildroot}/usr/share/man/${loc}/man{1..9}
	echo "%dir %ghost %lang(${loc}) /usr/share/man/${loc}" >> %{name}.man
	echo "%dir %ghost %lang(${loc}) /usr/share/man/${loc}/*" >> %{name}.man
done

> %{name}.lang
egrep -vh '^($|#)' %{SOURCE0} %{SOURCE1} | while read loc; do
	echo $loc | grep -q '@' && locale=${loc%%@*} || locale=$loc
	mkdir -p %{buildroot}/usr/share/locale/${loc}/LC_{MESSAGES,TIME}
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}" \
		>> %{name}.lang
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}/LC_MESSAGES" \
		>> %{name}.lang
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}/LC_TIME" \
		>> %{name}.lang
done

cat  %{name}.man %{name}.lang > %{name}.files

# multilib directories
%if "%{_lib}" != "lib"
  install -dv %{buildroot}/{usr/,}%{_lib}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.files
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
%if "%{_lib}" != "lib"
%dir /%{_lib}
%endif
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
%dir /usr
%dir /usr/bin
%dir /usr/include
%dir /usr/lib
%if "%{_lib}" != "lib"
%dir /usr/%{_lib}
%endif
%dir /usr/lib/lsb
%dir /usr/local
%dir /usr/local/bin
%dir /usr/local/include
%dir /usr/local/lib
%dir /usr/local/sbin
%dir /usr/local/share
%dir /usr/local/share/doc
%dir /usr/local/share/info
%dir /usr/local/share/locale
%dir /usr/local/share/man
%dir /usr/local/share/misc
%dir /usr/local/share/terminfo
%dir /usr/local/share/zoneinfo
%dir /usr/local/src
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/aclocal
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
%dir /usr/share/misc
%dir /usr/share/terminfo
%dir /usr/share/zoneinfo
%dir /usr/src
%dir /usr/src/kernels
%dir /var
%dir /var/cache
%dir /var/lib
%dir /var/lib/misc
%dir /var/lib/locate
%dir /var/local
%dir /var/lock
%dir /var/log
%dir /var/mail
%dir /var/opt
%dir /var/run
%dir /var/spool
%dir /var/spool/repackage
%attr(1777,root,root) %dir /var/tmp

%changelog
* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.4-1
- Merge iana-etc into base-layout

* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.3-1
- Merge base-files into base-layout

* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.2-1
- Remove /etc/sysconfig, add /etc/default

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-7
- Remove /usr/share/gtk-doc

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-6
- Add /{,usr}/lib/lsb directories, /etc/sysconfig

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-5
- Add /lib/modules, fix /usr/share/local/man

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-4
- Add more man dir locations to accomodate vim

* Sun Nov 01 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-3
- Add /usr/share/aclocal and /usr/share/gtk-doc/html

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-2
- Restructure man directories to be FHS compliant

* Sun Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Added a new locale

* Wed Sep 9 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-2
- Added /usr/share/dict as one of the base directories

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-1
- Initial version
