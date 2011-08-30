Summary: System V style init programs
Name: sysvinit
Version: 2.88dsf
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.nongnu.org/projects/sysvinit
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = f2ca149df1314a91f3007cccd7a0aa47d990de26

%description
System V style init programs that control system booting and shutdown.

%prep
%setup -q

%build
sed -i 's@Sending processes@& configured via /etc/inittab@g' \
    src/init.c
sed -i -e 's/utmpdump wall/utmpdump/' \
       -e 's/mountpoint.1 wall.1//' src/Makefile
%if "%{_lib}" != "lib"
sed -i 's@/lib/@/%{_lib}/@' src/Makefile
%endif
make -C src

%install
install -dv %{buildroot}/{bin,sbin,usr/bin,usr/include,usr/share/man/man{1,5,8}}
make ROOT=%{buildroot} -C src install
# Remove mountpoint, since util-linux provides a newer one
rm -f %{buildroot}/bin/mountpoint
rm -rfv %{buildroot}/usr/include

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/pidof
/sbin/bootlogd
/sbin/halt
/sbin/fstab-decode
/sbin/init
/sbin/killall5
/sbin/poweroff
/sbin/reboot
/sbin/runlevel
/sbin/shutdown
/sbin/sulogin
/sbin/telinit
/usr/bin/last
/usr/bin/lastb
/usr/bin/mesg
/usr/bin/utmpdump
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog
* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-3
- util-linux now provides /bin/mountpoint

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-2
- lsb-bootscripts now provide /etc/inittab

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-1
- Upgrade to 2.88dsf

* Sat Apr 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-2
- Add a default inittab file

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-1
- Initial version
