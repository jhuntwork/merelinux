Summary: Network Time Protocol utilities
Name: ntp
Version: 4.2.6p2
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.ntp.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/ntpd.init

BuildRequires: digest(%{SOURCE0}) = cf73cd85f248232c62f8029e6eb05938
BuildRequires: digest(%{SOURCE1}) = 89566c4ddf46fd78fdff5ae9f13340f0

%description
NTP is a protocol designed to synchronize the clocks of computers over a
network.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --with-binsubdir=sbin
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m 754 %{SOURCE1} %{buildroot}/etc/init.d/ntpd
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
/usr/sbin/remove_initd ntpd || /bin/true

%files
%defattr(-,root,root)
/etc/ntp.conf
/etc/init.d/ntpd
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
/usr/share/man/man1/ntp-keygen.1
/usr/share/man/man1/ntpd.1
/usr/share/man/man1/ntpdc.1
/usr/share/man/man1/ntpq.1
/usr/share/man/man1/ntpsnmpd.1
/usr/share/man/man1/sntp.1

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.6p2-1
- Initial version
