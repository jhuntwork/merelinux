Summary: Network Mapper
Name: nmap
Version: 5.51
Release: 1
Group: System Environment/Base
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://nmap.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 3415ad9a3915d7e162c9e91435cc35d9c73ac7f6
BuildRequires: openssl-devel
BuildRequires: pcre-devel

%description
Nmap ("Network Mapper") is a free and open source utility for network
exploration or security auditing.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --without-zenmap \
  --with-libpcap=included \
  --with-liblua=included
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/man/{jp,pt_PT,zh}
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/ncat
/usr/bin/ndiff
/usr/bin/nmap
/usr/bin/nping
/usr/share/man/de/man1/nmap.1.bz2
/usr/share/man/es/man1/nmap.1.bz2
/usr/share/man/fr/man1/nmap.1.bz2
/usr/share/man/hr/man1/nmap.1.bz2
/usr/share/man/hu/man1/nmap.1.bz2
/usr/share/man/it/man1/nmap.1.bz2
/usr/share/man/man1/ncat.1.bz2
/usr/share/man/man1/ndiff.1.bz2
/usr/share/man/man1/nmap.1.bz2
/usr/share/man/man1/nping.1.bz2
/usr/share/man/pl/man1/nmap.1.bz2
/usr/share/man/pt_BR/man1/nmap.1.bz2
/usr/share/man/ro/man1/nmap.1.bz2
/usr/share/man/ru/man1/nmap.1.bz2
/usr/share/man/sk/man1/nmap.1.bz2
/usr/share/ncat
/usr/share/nmap

%changelog
* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.51-1
- Initial version
