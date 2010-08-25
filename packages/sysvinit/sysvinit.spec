Summary: System V style init programs
Name: sysvinit
Version: 2.88dsf
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.nongnu.org/projects/sysvinit
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 6eda8a97b86e0a6f59dabbf25202aa6f

%description
System V style init programs that control system booting and shutdown.

%prep
%setup -q

%build
sed -i 's@Sending processes@& configured via /etc/inittab@g' \
    src/init.c
sed -i -e 's/utmpdump wall/utmpdump/' \
       -e 's/mountpoint.1 wall.1/mountpoint.1/' src/Makefile
%if "%{_lib}" != "lib"
sed -i 's@/lib/@/%{_lib}/@' src/Makefile
%endif
make -C src

%install
install -dv %{buildroot}/{bin,sbin,usr/bin,usr/include,usr/share/man/man{1,5,8}}
make ROOT=%{buildroot} -C src install
rm -rfv %{buildroot}/usr/include

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/mountpoint
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
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-2
- lsb-bootscripts now provide /etc/inittab

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-1
- Upgrade to 2.88dsf

* Sat Apr 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-2
- Add a default inittab file

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-1
- Initial version
