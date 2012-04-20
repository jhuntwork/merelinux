Summary: strace 
Name: strace
Version: 4.6
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sourceforge.net/projects/strace/
Source0: http://iweb.dl.sourceforge.net/project/strace/strace/4.6/strace-4.6.tar.xz 
Patch0: https://raw.github.com/rofl0r/sabotage/master/KEEP/strace-patch

BuildRequires: digest(sha1:%{SOURCE0}) = d84d6e215a65454aa5660e7b5c6200f6de39b89e

%description
strace is a system call tracer, i.e. a debugging tool which prints out<br> a
trace of all the system calls made by a another process/program.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%patch0 -p1
%{config_musl}

%build
export CFLAGS="-g -D_GNU_SOURCE -Os -pipe -DHAVE_LONG_LONG_OFF_T -DFPE_FLTUND=5 -DHAVE_SYS_REG_H -D__sched_priority=sched_priority -Dbool=int -DPTRACE_POKEUSR=PTRACE_POKEUSER -DMSG_EXCEPT=020000 -Dloff_t=int64_t"
export LDFLAGS="-g"
./configure \
  --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/info
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/strace
/usr/bin/strace-graph

%files extras
%defattr(-,root,root)
/usr/share/man/man1/strace.1.bz2

%changelog
* Tue Feb 07 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.6-1
- Initial version
