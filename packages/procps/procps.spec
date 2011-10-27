Summary: Procps - The /proc file system utilities
Name: procps
Version: 3.2.8
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://procps.sourceforge.net
Source0: http://procps.sourceforge.net/procps-3.2.8.tar.gz
Patch0: https://raw.github.com/jhuntwork/LightCube-OS/d313e70e4d4c3c42131313c47201d0fa55aa3047/packages/procps/procps-3.2.8-watch_unicode-1.patch
Patch1: https://raw.github.com/jhuntwork/LightCube-OS/2f0063747b84981d1f60598a333b2ca549562e15/packages/procps/procps-3.2.8-fix_HZ_errors-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = a0c86790569dec26b5d9037e8868ca907acc9829
BuildRequires: digest(sha1:%{PATCH0})  = 70eb76e7370448213130d5520d8132f0bd1c761f
BuildRequires: digest(sha1:%{PATCH1})  = ad48483cae06a8d0aca7944b11100b92cdc6b42c
BuildRequires: ncurses-devel

%description
procps is a number small useful utilities that give information about
processes using the /proc filesystem. The package includes the programs
ps, top, vmstat, w, kill, free, slabtop, and skill. 

%prep
%setup -q
%patch0 -p1
%patch1 -p1
# Fix a build problem with make-3.82
sed -i -e 's@\*/module.mk@proc/module.mk ps/module.mk@' Makefile

%build
# -O2 -s is default CFLAGS in package, modified to below to fit
# for optimization for size
make CFLAGS='-Os -s -pipe'

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

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
/usr/share/man/man1/free.1.bz2
/usr/share/man/man1/kill.1.bz2
/usr/share/man/man1/pgrep.1.bz2
/usr/share/man/man1/pkill.1.bz2
/usr/share/man/man1/pmap.1.bz2
/usr/share/man/man1/ps.1.bz2
/usr/share/man/man1/pwdx.1.bz2
/usr/share/man/man1/skill.1.bz2
/usr/share/man/man1/slabtop.1.bz2
/usr/share/man/man1/snice.1.bz2
/usr/share/man/man1/tload.1.bz2
/usr/share/man/man1/top.1.bz2
/usr/share/man/man1/uptime.1.bz2
/usr/share/man/man1/w.1.bz2
/usr/share/man/man1/watch.1.bz2
/usr/share/man/man5/sysctl.conf.5.bz2
/usr/share/man/man8/sysctl.8.bz2
/usr/share/man/man8/vmstat.8.bz2

%changelog
* Thu Oct 27 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.2.8-2
- Optimize for size

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
