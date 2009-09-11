Summary: Base directory layout
Name: base-layout
Version: 0.0
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/lang-iso
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/lang-exceptions

Requires(postun): /

%description
Provides an empty filesystem layout with all necessary
directories for a standard system.

%prep

%install
# Top-level directories
install -dv %{buildroot}/{bin,boot,dev,etc,home,lib,media,mnt,opt,proc,root,sbin,srv,sys,tmp,usr,var}

install -dv %{buildroot}/media/{floppy,cdrom}
install -dv %{buildroot}/usr/{,local/}{bin,include,lib,sbin,src}
install -dv %{buildroot}/usr/{,local/}share/{dict,doc,info,locale,man}
install -dv %{buildroot}/usr/{,local/}share/{misc,terminfo,zoneinfo}
install -dv %{buildroot}/usr/{,local/}share/man/man{1..8}
for dir in %{buildroot}/usr %{buildroot}/usr/local
  do ln -sv share/{man,doc,info} $dir
done
install -dv %{buildroot}/var/{lock,log,mail,run,spool,tmp}
install -dv %{buildroot}/var/spool/repackage
install -dv %{buildroot}/var/{opt,cache,lib/{hwclock,misc,locate},local}

> %{name}.lang
egrep -vh '^($|#)' %{SOURCE0} %{SOURCE1} | while read loc; do
	echo $loc | grep -q '@' && locale=${loc%%@*} || locale=$loc
	mkdir -p ${RPM_BUILD_ROOT}/usr/share/locale/${loc}/LC_{MESSAGES,TIME}
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}" \
		>> %{name}.lang
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}/LC_MESSAGES" \
		>> %{name}.lang
	echo "%dir %ghost %lang(${locale}) /usr/share/locale/${loc}/LC_TIME" \
		>> %{name}.lang
done

cat %{name}.lang > %{name}.files

# multilib directories
%if "%{_lib}" != "lib"
  install -dv %{buildroot}/{usr/,}%{_lib}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.files
%defattr(-,root,root)
/usr/doc
/usr/info
/usr/man
/usr/local/doc
/usr/local/info
/usr/local/man
%dir /
%dir /bin
%dir /boot
%dir /dev
%dir /etc
%dir /home
%dir /lib
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
%dir /usr/local/share/man/man1
%dir /usr/local/share/man/man2
%dir /usr/local/share/man/man3
%dir /usr/local/share/man/man4
%dir /usr/local/share/man/man5
%dir /usr/local/share/man/man6
%dir /usr/local/share/man/man7
%dir /usr/local/share/man/man8
%dir /usr/local/share/misc
%dir /usr/local/share/terminfo
%dir /usr/local/share/zoneinfo
%dir /usr/local/src
%dir /usr/sbin
%dir /usr/share
%dir /usr/share/dict
%dir /usr/share/doc
%dir /usr/share/info
%dir /usr/share/locale
%dir /usr/share/man
%dir /usr/share/man/man1
%dir /usr/share/man/man2
%dir /usr/share/man/man3
%dir /usr/share/man/man4
%dir /usr/share/man/man5
%dir /usr/share/man/man6
%dir /usr/share/man/man7
%dir /usr/share/man/man8
%dir /usr/share/misc
%dir /usr/share/terminfo
%dir /usr/share/zoneinfo
%dir /usr/src
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
* Wed Sep 9 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-2
- Added /usr/share/dict as one of the base directories

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-1
- Initial version
