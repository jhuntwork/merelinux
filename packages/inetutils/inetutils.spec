Summary: GNU Inetutils
Name: inetutils
Version: 1.7
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/inetutils
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = a1d5a01b0ab8a7e596ac4cff0cce7129

%description
%{name} is a collection of common networking programs including ftp,
telnet, ping, hostname and traceroute

%prep
%setup -q

%build
./configure --prefix=/usr --libexecdir=/usr/sbin \
    --localstatedir=/var --disable-ifconfig \
    --disable-logger --disable-syslogd --disable-whois \
    --disable-servers
make

%install
make DESTDIR=%{buildroot} install
mkdir -v %{buildroot}/bin
mv -v %{buildroot}/usr/bin/ping %{buildroot}/bin
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/inetutils.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/inetutils.info /usr/share/info/dir

%files
%defattr(-,root,root)
/bin/ping
/usr/bin/ftp
/usr/bin/hostname
/usr/bin/ping6
/usr/bin/rcp
/usr/bin/rexec
/usr/bin/rlogin
/usr/bin/rsh
/usr/bin/talk
/usr/bin/telnet
/usr/bin/tftp
/usr/bin/traceroute
/usr/share/info/inetutils.info
/usr/share/man/man1/ftp.1
/usr/share/man/man1/hostname.1
/usr/share/man/man1/rcp.1
/usr/share/man/man1/rexec.1
/usr/share/man/man1/rlogin.1
/usr/share/man/man1/rsh.1
/usr/share/man/man1/talk.1
/usr/share/man/man1/telnet.1
/usr/share/man/man1/tftp.1
/usr/share/man/man1/traceroute.1
/usr/share/man/man1/ping.1

%changelog
* Mon Dec 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7-1
- Upgrade to 1.7

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6-2
- Use FHS compatible info directories

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6-1
- Initial version
