Summary: Procps - The /proc file system utilities
Name: procps
Version: 3.2.8
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://procps.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-watch_unicode-1.patch

Requires: base-layout, glibc

%description
%{name} is a number small useful utilities that give information about
processes using the /proc filesystem. The package includes the programs
ps, top, vmstat, w, kill, free, slabtop, and skill. 

%prep
%setup -q

%build
patch -Np1 -i %{SOURCE1}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/bin/kill
/bin/ps
/%{_lib}/libproc-3.2.8.so
/sbin/sysctl
/usr/bin/free
/usr/bin/pgrep
/usr/bin/pkill
/usr/bin/pmap
/usr/bin/pwdx
/usr/bin/skill
/usr/bin/slabtop
/usr/bin/snice
/usr/bin/tload
/usr/bin/top
/usr/bin/uptime
/usr/bin/vmstat
/usr/bin/w
/usr/bin/watch
/usr/share/man/man1/free.1
/usr/share/man/man1/kill.1
/usr/share/man/man1/pgrep.1
/usr/share/man/man1/pkill.1
/usr/share/man/man1/pmap.1
/usr/share/man/man1/ps.1
/usr/share/man/man1/pwdx.1
/usr/share/man/man1/skill.1
/usr/share/man/man1/slabtop.1
/usr/share/man/man1/snice.1
/usr/share/man/man1/tload.1
/usr/share/man/man1/top.1
/usr/share/man/man1/uptime.1
/usr/share/man/man1/w.1
/usr/share/man/man1/watch.1
/usr/share/man/man5/sysctl.conf.5
/usr/share/man/man8/sysctl.8
/usr/share/man/man8/vmstat.8

%changelog
* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
