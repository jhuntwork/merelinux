Summary: GNU Wget
Name: wget
Version: 1.13.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/wget
Source0: http://ftp.gnu.org/gnu/wget/wget-%{version}.tar.xz

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
%{config_musl}
sed -i 's@/usr/bin/env@/bin/env@' doc/texi2pod.pl
sed -i "/netinet\/in\.h/s@.*@&\n#define IN6_ARE_ADDR_EQUAL(a,b) ((((__const uint32_t *) (a))[0] == ((__const uint32_t *) (b))[0]) \&\& (((__const uint32_t *) (a))[1] == ((__const uint32_t *) (b))[1]) \&\& (((__const uint32_t *) (a))[2] == ((__const uint32_t *) (b))[2]) \&\& (((__const uint32_t *) (a))[3] == ((__const uint32_t *) (b))[3]))@" src/host.c

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --prefix=/ \
  --sysconfdir=/etc \
  --with-ssl=openssl
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
install -d %{buildroot}/etc
echo "
# Set the certificate authority bundle file to the location provided by OpenSSL
ca_certificate = /etc/ssl/certs/ca-bundle.crt" >> \
  %{buildroot}/etc/wgetrc
rm -rf %{buildroot}/lib
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/wget
%config /etc/wgetrc
/share/man/man1/wget.1.bz2

%changelog
* Thu Apr 19 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.13.4-1
- Initial version
