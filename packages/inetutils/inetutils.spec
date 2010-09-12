Summary: GNU Inetutils
Name: inetutils
# Using a dev snapshot due to fixes in ifconfig - looking forward to 1.9
Version: 20100910
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/inetutils
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 2a1ca7f1e72ec26861e44efd8cf5f2111616684e
BuildRequires: readline-devel
BuildRequires: ncurses-devel

%description
Inetutils is a collection of common networking programs including ftp,
telnet, ping, hostname and traceroute

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libexecdir=/usr/sbin \
  --localstatedir=/var \
  --disable-logger \
  --disable-syslogd \
  --disable-whois \
  --disable-servers
make

%install
make DESTDIR=%{buildroot} install
mkdir -v %{buildroot}/{,s}bin
mv -v %{buildroot}/usr/bin/ping %{buildroot}/bin
mv -v %{buildroot}/usr/bin/hostname %{buildroot}/bin
mv -v %{buildroot}/usr/bin/ifconfig %{buildroot}/bin
mv -v %{buildroot}/usr/bin/traceroute %{buildroot}/sbin
rm -f %{buildroot}/usr/share/info/dir
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/inetutils.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/inetutils.info /usr/share/info/dir

%files
%defattr(-,root,root)
/bin/hostname
/bin/ifconfig
/bin/ping
/sbin/traceroute
/usr/bin/ftp
/usr/bin/ping6
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
/usr/share/man/man1/ifconfig.1.bz2
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
