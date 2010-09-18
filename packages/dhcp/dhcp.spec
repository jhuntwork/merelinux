Summary: DHCP
Name: dhcp
Version: 4.1.1
Release: 1
Group: System Environment/Base
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.isc.org/software/dhcp
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-P1.tar.gz
Source1: http://dev.lightcube.us/sources/%{name}/dhcpd.init

BuildRequires: digest(sha1:%{SOURCE0}) = e9e756df09502f6666cd79bdf0ab3af0f92b41b0
BuildRequires: digest(sha1:%{SOURCE1}) = e7dd5ed50ae49f3e9d9e86e705d660804d615383

%description
ISC's DHCP software is the most widely used open source DHCP implementation.
It provides both a DHCP server and client tool.

%package server
Summary: The DHCP server
Group: Services
Requires: %{name} = %{version}

%description server
The DHCP server

%package devel
Summary: Headers and Libraries for developing with DHCP
Group: Development/Libraries
Requires: %{name} = %{version}

%description devel
Headers and Libraries for developing with DHCP

%prep
%setup -q -n %{name}-%{version}-P1

%build
export CFLAGS="-g -O2  -Wall -pipe -fno-strict-aliasing"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --with-srv-lease-file=/var/lib/dhcp/dhcpd.leases \
  --with-srv6-lease-file=/var/lib/dhcp/dhcpd6.leases \
  --with-cli-lease-file=/var/lib/dhcp/dhclient.leases \
  --with-cli6-lease-file=/var/lib/dhcp/dhclient6.leases
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/{sbin,etc/init.d}
install -dv %{buildroot}/var/lib/dhcp
mv -v %{buildroot}/usr/sbin/dhclient %{buildroot}/sbin
cat > %{buildroot}/etc/dhclient.conf << "EOF"
# See dhclient.conf.5 man page for more configuration options
request subnet-mask, broadcast-address, time-offset, routers,
     domain-name, domain-name-servers, host-name;
require subnet-mask, domain-name-servers;
EOF
sed -e '/^[ \t]*route/s@route@\$\{ip\} &@' \
    -e 's@ gw @ via @g' \
    client/scripts/linux > %{buildroot}/sbin/dhclient-script
install %{SOURCE1} %{buildroot}/etc/init.d/dhcpd
%{compress_man}

%preun server
/usr/sbin/remove_initd dhcpd || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/dhclient.conf
/sbin/dhclient
%attr(0755,root,root) /sbin/dhclient-script
/usr/share/man/man5/dhclient.leases.5.bz2
/usr/share/man/man5/dhcp-eval.5.bz2
/usr/share/man/man5/dhclient.conf.5.bz2
/usr/share/man/man8/dhclient-script.8.bz2
/usr/share/man/man8/dhclient.8.bz2
/var/lib/dhcp

%files devel
%defattr(-,root,root)
/usr/include/dhcpctl
/usr/include/isc-dhcp
/usr/include/omapip
/usr/%{_lib}/libdhcpctl.a
/usr/%{_lib}/libdst.a
/usr/%{_lib}/libomapi.a
/usr/share/man/man3/dhcpctl.3.bz2
/usr/share/man/man3/omapi.3.bz2

%files server
%defattr(-,root,root)
%config /etc/dhcpd.conf
/etc/init.d/dhcpd
/usr/bin/omshell
/usr/sbin/dhcpd
/usr/sbin/dhcrelay
/usr/share/man/man1/omshell.1.bz2
/usr/share/man/man5/dhcp-options.5.bz2
/usr/share/man/man5/dhcpd.conf.5.bz2
/usr/share/man/man5/dhcpd.leases.5.bz2
/usr/share/man/man8/dhcpd.8.bz2
/usr/share/man/man8/dhcrelay.8.bz2

%changelog
* Fri Sep 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.1-1
- Initial version
