Summary: Base directory layout
Name: base-layout
Version: 0.1
Release: 7
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Source0: http://dev.lightcube.us/sources/%{name}/lang-iso
Source1: http://dev.lightcube.us/sources/%{name}/lang-exceptions

Requires(postun): /
BuildRequires: digest(sha1:%{SOURCE0}) = 9b091c035b2959b085ef7e46f242451bce844d4c
BuildRequires: digest(sha1:%{SOURCE1}) = 890e047e6b8a2a34f84f0214bbd4a6fcf7bd1d05

%description
Provides an empty filesystem layout with all necessary
directories for a standard system.

%prep

%install
# Top-level directories
install -dv %{buildroot}/{bin,boot,dev,etc/sysconfig,home,lib,media,mnt,opt,proc,root,sbin,srv,sys,tmp,usr,var}
install -dv %{buildroot}/lib/{lsb,modules}
install -dv %{buildroot}/media/{floppy,cdrom}
install -dv %{buildroot}/usr/{,local/}{bin,include,lib/lsb,sbin,src}
install -dv %{buildroot}/usr/src/kernels
install -dv %{buildroot}/usr/{,local/}share/{aclocal,dict,doc,info,locale}
install -dv %{buildroot}/usr/{,local/}share/{man,misc,terminfo,zoneinfo}
install -dv %{buildroot}/var/{lock,log,mail,run,spool,tmp}
install -dv %{buildroot}/var/spool/repackage
install -dv %{buildroot}/var/{opt,cache,lib/{hwclock,misc,locate},local}

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
%dir /etc/sysconfig
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
