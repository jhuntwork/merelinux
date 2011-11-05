Summary: Net:Iproute2
Name: iproute2
Version: 2.6.37
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.linuxfoundation.org/collaborate/workgroups/networking/iproute2
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 7852fb66fb745dc3c1fabee24d7d8ff017c48d36
BuildRequires: db-devel
BuildRequires: flex

%description
Iproute2 is a collection of utilities for controlling
TCP/IP networking and traffic control in Linux

%prep
%setup -q
sed -i 's@-O2@-Os -pipe@' Makefile

%build
make %{PMFLAGS} DESTDIR= LIBDIR=/%{_lib}

%install
make DESTDIR=%{buildroot} SBINDIR=/sbin MANDIR=/usr/share/man \
     LIBDIR=/%{_lib} DOCDIR=/usr/share/doc/%{name}-%{version} install
install -dv %{buildroot}/var/lib/arpd
rm -v %{buildroot}/usr/share/man/man3/libnetlink.3
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/iproute2
/%{_lib}/tc
/sbin/arpd
/sbin/ctstat
/sbin/genl
/sbin/ifcfg
/sbin/ifstat
/sbin/ip
/sbin/lnstat
/sbin/nstat
/sbin/routef
/sbin/routel
/sbin/rtacct
/sbin/rtmon
/sbin/rtpr
/sbin/rtstat
/sbin/ss
/sbin/tc
/usr/share/doc/%{name}-%{version}
/usr/share/man/man8/arpd.8.bz2
/usr/share/man/man8/ctstat.8.bz2
/usr/share/man/man8/ip.8.bz2
/usr/share/man/man8/lnstat.8.bz2
/usr/share/man/man8/nstat.8.bz2
/usr/share/man/man8/routef.8.bz2
/usr/share/man/man8/routel.8.bz2
/usr/share/man/man8/rtacct.8.bz2
/usr/share/man/man8/rtstat.8.bz2
/usr/share/man/man8/rtmon.8.bz2
/usr/share/man/man8/ss.8.bz2
/usr/share/man/man8/tc-bfifo.8.bz2
/usr/share/man/man8/tc-cbq-details.8.bz2
/usr/share/man/man8/tc-cbq.8.bz2
/usr/share/man/man8/tc-drr.8.bz2
/usr/share/man/man8/tc-htb.8.bz2
/usr/share/man/man8/tc-pfifo.8.bz2
/usr/share/man/man8/tc-pfifo_fast.8.bz2
/usr/share/man/man8/tc-prio.8.bz2
/usr/share/man/man8/tc-red.8.bz2
/usr/share/man/man8/tc-sfq.8.bz2
/usr/share/man/man8/tc-tbf.8.bz2
/usr/share/man/man8/tc.8.bz2
%dir /var/lib/arpd

%changelog
* Sat Nov 05 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.37-2
- Optimize for size
- Move arpd back into main package since db is part of base system

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.37-1
- Upgrade to 2.6.37

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.35-1
- Upgrade to 2.6.35

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.33-2
- Separate the aprd binary due to its dependence on db

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.33-1
- Upgraded to 2.6.33-1

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
