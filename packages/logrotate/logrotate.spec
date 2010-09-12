Summary: Log Rotation Tool
Name: logrotate
Version: 3.7.9
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://fedorahosted.org/logrotate
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = eeba9dbca62a9210236f4b83195e4ea5
BuildRequires: popt-devel

%description
The logrotate utility is designed to simplify the administration of log files
on a system which generates a lot of log files. Logrotate allows for the
automatic rotation compression, removal and mailing of log files. Logrotate can
be set to handle a log file daily, weekly, monthly or when the log file gets to
a certain size.

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
make BASEDIR="/usr"

%install
make PREFIX=%{buildroot} MANDIR="/usr/share/man" install
install -dv %{buildroot}/etc/logrotate.d
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/logrotate.d
/usr/sbin/logrotate
/usr/share/man/man5/logrotate.conf.5.bz2
/usr/share/man/man8/logrotate.8.bz2

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.7.9-1
- Initial version
