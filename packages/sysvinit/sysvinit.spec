Summary: System V style init programs
Name: sysvinit
Version: 2.88dsf
Release: 1
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
install -dv %{buildroot}/etc
cat > %{buildroot}/etc/inittab << "EOF"
#Begin /etc/inittab

id:3:initdefault:

si::sysinit:/etc/rc.d/init.d/rc sysinit

l0:0:wait:/etc/rc.d/init.d/rc 0
l1:S1:wait:/etc/rc.d/init.d/rc 1
l2:2:wait:/etc/rc.d/init.d/rc 2
l3:3:wait:/etc/rc.d/init.d/rc 3
l4:4:wait:/etc/rc.d/init.d/rc 4
l5:5:wait:/etc/rc.d/init.d/rc 5
l6:6:wait:/etc/rc.d/init.d/rc 6

ca:12345:ctrlaltdel:/sbin/shutdown -t1 -a -r now

su:S016:once:/sbin/sulogin

1:2345:respawn:/sbin/agetty tty1 9600
2:2345:respawn:/sbin/agetty tty2 9600
3:2345:respawn:/sbin/agetty tty3 9600
4:2345:respawn:/sbin/agetty tty4 9600
5:2345:respawn:/sbin/agetty tty5 9600
6:2345:respawn:/sbin/agetty tty6 9600

# End /etc/inittab
EOF
rm -rfv %{buildroot}/usr/include

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/mountpoint
/bin/pidof
/etc/inittab
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
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.88dsf-1
- Upgrade to 2.88dsf

* Sat Apr 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-2
- Add a default inittab file

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.86-1
- Initial version
