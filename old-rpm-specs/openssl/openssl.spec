Summary: OpenSSL
Name: openssl
Version: 1.0.1
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.org
Source0: http://www.openssl.org/source/openssl-%{version}.tar.gz
Source1: mkcabundle.pl
Patch0:  openssl-1.0.1-parallel-build.patch 

BuildRequires: digest(sha1:%{SOURCE0}) = a6476d33fd38c2e7dfb438d1e3be178cc242c907
BuildRequires: digest(sha1:%{SOURCE1}) = b3fb118d6eb1129865e8a448662806e6f69a5e03
BuildRequires: cvs
#BuildRequires: perl
BuildRequires: zlib-devel

%description
OpenSSL provides a robust, commercial-grade, full-featured, and Open Source
toolkit implementing the Secure Sockets Layer (SSL v2/v3) and Transport Layer
Security (TLS v1) protocols as well as a full-strength general purpose
cryptography library. 

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

%package misc
Summary: Miscellaneous OpenSSL related tools
Group: System Environment/Utilities
Requires: %{name} >= %{version}

%description misc
Miscellaneous OpenSSL related tools

%prep
%setup -q
chmod +x %{SOURCE1}
%patch0 -p1
sed -i '/^"linux-x86_64/s/-DTERMIO/-DTERMIOS/' Configure
sed -i '/^"linux-elf/s/-DTERMIO/-DTERMIOS/' Configure
sed -i 's/defined(linux)/0/' crypto/ui/ui_openssl.c

%build
# Without dso, a suffix of 'bad' is used when installing engine libs
# Can get around it by including the string DSO_BEOS in CFLAGS
./config \
  --prefix=/ \
  --libdir=/lib \
  --openssldir=/etc/ssl \
  shared zlib no-dso -D_GNU_SOURCE -pipe -D_HACK_DSO_BEOS
make %{PMFLAGS}

%install
make INSTALL_PREFIX=%{buildroot} MANDIR=/share/man install
install -dv %{buildroot}/etc/ssl/certs
%{SOURCE1} > %{buildroot}/etc/ssl/certs/ca-bundle.crt
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /etc/ssl
/etc/ssl/certs
/etc/ssl/openssl.cnf
/etc/ssl/private
/bin/openssl
/lib/libcrypto.so.1.0.0
/lib/libssl.so.1.0.0
/share/man/man1/*.bz2
/share/man/man5/*.bz2
/share/man/man7/*.bz2

%files devel
%defattr(-,root,root)
/include/openssl
/lib/libcrypto.a
/lib/libcrypto.so
/lib/libssl.a
/lib/libssl.so
/lib/engines
/lib/pkgconfig/libcrypto.pc
/lib/pkgconfig/libssl.pc
/lib/pkgconfig/openssl.pc
/share/man/man3/*.bz2

%files misc
%defattr(-,root,root)
/bin/c_rehash
/etc/ssl/misc

%changelog
* Thu Apr 19 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.1-1
- Initial version
