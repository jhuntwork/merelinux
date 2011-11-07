Summary: NET-3 Network Tools
Name: net-tools
Version: 1.60
Release: 2
Group: System Environment/Base
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/inetutils
Source0: http://iweb.dl.sourceforge.net/project/net-tools/net-tools-1.60.tar.bz2
Patch0:  https://raw.github.com/jhuntwork/LightCube-OS/master/packages/net-tools/debian-fixes.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 944fb70641505d5d1139dba3aeb81ba124574b83
BuildRequires: digest(sha1:%{PATCH0})  = 0342a1ff113fac94a222566c0c093830a851caf1

%description
Net-tools is A collection of programs that form the base set of the NET-3
networking distribution for the Linux operating system. This package includes
arp, ifconfig, ipmaddr, iptunnel, mii-tool, nameif, netstat, plipconfig, rarp,
route and slattach.

%prep
%setup -q
%patch0 -p1
sed -i 's@-O2@-Os -pipe@' Makefile

%build
yes "" | make config
make %{PMFLAGS}

%install
make BASEDIR=%{buildroot} install
# Remove hostname, provided in inetutils
rm -f %{buildroot}/bin/hostname
rm -f %{buildroot}/usr/share/man/man1/hostname.1
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/dnsdomainname
/bin/domainname
/bin/netstat
/bin/nisdomainname
/bin/ypdomainname
/sbin/arp
/sbin/ifconfig
/sbin/ipmaddr
/sbin/iptunnel
/sbin/mii-tool
/sbin/nameif
/sbin/plipconfig
/sbin/rarp
/sbin/route
/sbin/slattach
/usr/share/man/man1/dnsdomainname.1.bz2
/usr/share/man/man1/domainname.1.bz2
/usr/share/man/man1/nisdomainname.1.bz2
/usr/share/man/man1/ypdomainname.1.bz2
/usr/share/man/man5/ethers.5.bz2
/usr/share/man/man8/arp.8.bz2
/usr/share/man/man8/ifconfig.8.bz2
/usr/share/man/man8/mii-tool.8.bz2
/usr/share/man/man8/nameif.8.bz2
/usr/share/man/man8/netstat.8.bz2
/usr/share/man/man8/plipconfig.8.bz2
/usr/share/man/man8/rarp.8.bz2
/usr/share/man/man8/route.8.bz2
/usr/share/man/man8/slattach.8.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.60-2
- Optimize for size

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.60-1
- Initial version
