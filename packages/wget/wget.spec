Summary: GNU Wget
Name: wget
Version: 1.13.4
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/wget
Source0: ftp://ftp.gnu.org/gnu/wget/wget-1.13.4.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = a55ecf582fa58e8bb50c3952f6786f33f498f42a
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
GNU Wget is a free software package for retrieving files using HTTP, HTTPS
and FTP, the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs,
terminals without X-Windows support, etc.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --with-ssl=openssl
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
echo "
# Set the certificate authority bundle file to the location provided by OpenSSL
ca_certificate = /etc/ssl/certs/ca-bundle.crt" >> \
  %{buildroot}/etc/wgetrc
%find_lang %{name}
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/wget.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/wget.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/wget
%config /etc/wgetrc
/usr/share/info/wget.info
/usr/share/man/man1/wget.1.bz2

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.13.4-2
- Add default configuration for ca bundle included with OpenSSL

* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.13.4-1
- Upgrade to 1.13.4
- Optimize for size

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.12-1
- Initial version
