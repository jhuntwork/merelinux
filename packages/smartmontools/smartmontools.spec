Summary: smartmontools
Name: smartmontools
Version: 5.39.1
Release: 1
Group: Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sourceforge.net/apps/trac/smartmontools/wiki
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ea0489c9234832f63ac0d4b4c0bd81133b4eb9e9

%description
smartmontools contains utility programs (smartctl, smartd) to control/monitor
storage systems using the Self-Monitoring, Analysis and Reporting Technology
System (S.M.A.R.T.) built into most modern ATA and SCSI disks. It is derived
from smartsuite.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --with-initscriptdir=/etc/init.d \
  --enable-savestates \
  --enable-attributelog
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -rf %{buildroot}/usr/share/doc
install -dv %{buildroot}/var/lib/smartmontools

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/init.d/smartd
%config /etc/smartd.conf
/usr/sbin/smartctl
/usr/sbin/smartd
/usr/share/man/man5/smartd.conf.5.bz2
/usr/share/man/man8/smartctl.8.bz2
/usr/share/man/man8/smartd.8.bz2
/var/lib/smartmontools

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.39.1-1
- Initial version
