Summary: Network Time Protocol utilities
Name: ntp
Version: 4.2.6p4
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.ntp.org
Source0: http://www.eecis.udel.edu/~ntp/ntp_spool/ntp4/ntp-4.2/ntp-4.2.6p4.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/ntp/ntpd.init

BuildRequires: digest(sha1:%{SOURCE0}) = b53c4565c5d1c37494584d4fb826f82ffea285cf
BuildRequires: digest(sha1:%{SOURCE1}) = fb8868cd559a97a8e7dc1397617935f3b42f4f70

%description
NTP is a protocol designed to synchronize the clocks of computers over a
network.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --with-binsubdir=sbin
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}
install -dv %{buildroot}/etc/init.d
install -m 0754 %{SOURCE1} %{buildroot}/etc/init.d/ntpd
cat > %{buildroot}/etc/ntp.conf << "EOF"
driftfile /var/cache/ntp.drift
pidfile   /var/run/ntpd.pid
server 0.pool.ntp.org
server 1.pool.ntp.org
server 2.pool.ntp.org
server 3.pool.ntp.org
EOF

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install_initd ntpd

%preun
/usr/sbin/remove_initd ntpd 2>&1 || /bin/true

%files
%defattr(-,root,root)
%config /etc/ntp.conf
%config /etc/init.d/ntpd
/usr/sbin/ntp-keygen
/usr/sbin/ntp-wait
/usr/sbin/ntpd
/usr/sbin/ntpdate
/usr/sbin/ntpdc
/usr/sbin/ntpq
/usr/sbin/ntptime
/usr/sbin/ntptrace
/usr/sbin/sntp
/usr/sbin/tickadj
/usr/share/man/man1/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.6p4-1
- Upgrade to 4.2.6p4
- Optimize for size

* Mon Aug 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.6p3-1
- Upgrade to 4.2.6p3
- Fixes to init script

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.6p2-1
- Initial version
