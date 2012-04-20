Summary: Log Rotation Tool
Name: logrotate
Version: 3.8.1
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://fedorahosted.org/logrotate
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 1df36cee76a9c4c7438f35ca3599a7bdd68a09b5
BuildRequires: popt-devel

%description
The logrotate utility is designed to simplify the administration of log files
on a system which generates a lot of log files. Logrotate allows for the
automatic rotation compression, removal and mailing of log files. Logrotate can
be set to handle a log file daily, weekly, monthly or when the log file gets to
a certain size.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q

%build
make BASEDIR="/usr" LFS='-Os -pipe -D_GNU_SOURCE'

%install
make PREFIX=%{buildroot} MANDIR="/usr/share/man" install
install -dv %{buildroot}/etc/logrotate.d
install -dv %{buildroot}/usr/lib/logrotate
install -m 0754 examples/logrotate.cron \
  %{buildroot}/usr/lib/logrotate/logrotate.cron.sh
sed 's@^#compress@compress@' examples/logrotate-default \
  > %{buildroot}/etc/logrotate.conf
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/logrotate.conf
%dir /etc/logrotate.d
/usr/lib/logrotate
/usr/sbin/logrotate

%files extras
%defattr(-,root,root)
/usr/share/man/man5/logrotate.conf.5.bz2
/usr/share/man/man8/logrotate.8.bz2

%changelog
* Wed Feb 01 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.8.1-1
- Initial version
