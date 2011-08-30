Summary: GNU Inetutils
Name: inetutils
Version: 1.8
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/inetutils
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 598445859b511f73681e4d74a41d65cd6ae0f83e
BuildRequires: readline-devel
BuildRequires: ncurses-devel

%description
Inetutils is a collection of common networking programs including ftp,
telnet, ping, hostname and traceroute

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libexecdir=/usr/sbin \
  --localstatedir=/var \
  --disable-ifconfig \
  --disable-logger \
  --disable-syslogd \
  --disable-whois \
  --disable-servers
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
mkdir -v %{buildroot}/{,s}bin
mv -v %{buildroot}/usr/bin/ping %{buildroot}/bin
mv -v %{buildroot}/usr/bin/ping6 %{buildroot}/bin
mv -v %{buildroot}/usr/bin/hostname %{buildroot}/bin
mv -v %{buildroot}/usr/bin/traceroute %{buildroot}/sbin
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/inetutils.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/inetutils.info /usr/share/info/dir

%files
%defattr(-,root,root)
/bin/hostname
/bin/ping
/bin/ping6
/sbin/traceroute
/usr/bin/ftp
/usr/bin/rcp
/usr/bin/rexec
/usr/bin/rlogin
/usr/bin/rsh
/usr/bin/talk
/usr/bin/telnet
/usr/bin/tftp
/usr/share/info/inetutils.info
/usr/share/man/man1/ftp.1.bz2
/usr/share/man/man1/hostname.1.bz2
/usr/share/man/man1/rcp.1.bz2
/usr/share/man/man1/rexec.1.bz2
/usr/share/man/man1/rlogin.1.bz2
/usr/share/man/man1/rsh.1.bz2
/usr/share/man/man1/talk.1.bz2
/usr/share/man/man1/telnet.1.bz2
/usr/share/man/man1/tftp.1.bz2
/usr/share/man/man1/traceroute.1.bz2
/usr/share/man/man1/ping.1.bz2
/usr/share/man/man1/ping6.1.bz2

%changelog
* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8-2
- Revert to 1.8. ifconfig provided in net-tools

* Fri Sep 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20100910-1
- Upgrade to 20100910

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8-1
- Upgrade to 1.8

* Mon Dec 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7-1
- Upgrade to 1.7

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6-2
- Use FHS compatible info directories

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6-1
- Initial version
