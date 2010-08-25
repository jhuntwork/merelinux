Summary: Kernel and system logging daemons
Name: sysklogd
Version: 1.5
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.infodrom.org/projects/sysklogd
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = e053094e8103165f98ddafe828f6ae4b

%description
%{name} implements two system log daemons. The syslogd daemon is an enhanced
version of the standard Berkeley utility program. This daemon is responsible
for providing logging of messages received from programs and facilities on
the local host as well as from remote hosts. The klogd daemon listens to
kernel message sources and is responsible for prioritizing and processing
operating system messages. The klogd daemon can run as a client of syslogd
or optionally as a standalone program

%prep
%setup -q

%build
make

%install
install -dv %{buildroot}/{sbin,usr/share/man/man{5,8}}
make prefix=%{buildroot} BINDIR=%{buildroot}/sbin install
install -dv %{buildroot}/etc
cat > %{buildroot}/etc/syslog.conf << "EOF"
# Begin /etc/syslog.conf

auth,authpriv.* -/var/log/auth.log
*.*;auth,authpriv.none -/var/log/sys.log
daemon.* -/var/log/daemon.log
kern.* -/var/log/kern.log
mail.* -/var/log/mail.log
user.* -/var/log/user.log
*.emerg *
cron.* -/var/log/cron.log

# End /etc/syslog.conf
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/syslog.conf
/sbin/klogd
/sbin/syslogd
/usr/share/man/man5/syslog.conf.5
/usr/share/man/man8/klogd.8
/usr/share/man/man8/sysklogd.8
/usr/share/man/man8/syslogd.8

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5-2
- Add entry for cron log

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5-1
- Initial version
