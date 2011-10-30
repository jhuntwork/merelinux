Summary: OpenSSL
Name: openssl
Version: 1.0.0e
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.org
Source0: http://www.openssl.org/source/openssl-1.0.0e.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/6ec15eae837af05a61f214bf3789004f22a51149/packages/openssl/mkcabundle.pl

BuildRequires: digest(sha1:%{SOURCE0}) = 235eb68e5a31b0f7a23bc05f52d7a39c596e2e69
BuildRequires: digest(sha1:%{SOURCE1}) = e20db4e2e8a983e39bf19ce349da091abf62c7c1
BuildRequires: zlib-devel
BuildRequires: cvs

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
sed -i 's@-O3 -Wall@& -Os -pipe -fno-strict-aliasing@' Configure

%build
./config \
  --openssldir=/etc/ssl \
  --prefix=/usr \
  shared zlib-dynamic
# Doesn't make use of parallel builds - don't use %{PMFLAGS}
make LIBDIR=%{_lib} MANDIR=/usr/share/man

%install
make INSTALL_PREFIX=%{buildroot} LIBDIR=%{_lib} MANDIR=/usr/share/man install
install -dv %{buildroot}/etc/ssl/certs
%{SOURCE1} > %{buildroot}/etc/ssl/certs/ca-bundle.crt
%{compress_man}
%{strip}
find %{buildroot} -name "passwd.1.bz2" -delete
mv -v %{buildroot}/usr/share/man/man3/{,SSL-}threads.3.bz2

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /etc/ssl
/etc/ssl/certs
/etc/ssl/openssl.cnf
/etc/ssl/private
/usr/bin/c_rehash
/usr/bin/openssl
/usr/%{_lib}/libcrypto.so.1.0.0
/usr/%{_lib}/libssl.so.1.0.0
/usr/share/man/man1/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man7/*.bz2

%files devel
%defattr(-,root,root)
/usr/include/openssl
/usr/%{_lib}/libcrypto.a
/usr/%{_lib}/libcrypto.so
/usr/%{_lib}/libssl.a
/usr/%{_lib}/libssl.so
/usr/%{_lib}/engines
/usr/%{_lib}/pkgconfig/libcrypto.pc
/usr/%{_lib}/pkgconfig/libssl.pc
/usr/%{_lib}/pkgconfig/openssl.pc
/usr/share/man/man3/*.bz2

%files misc
%defattr(-,root,root)
/etc/ssl/misc

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0e-3
- Upgrade to 1.0.0e - security and bug fixes
- Optimize for size
- Include a CA certificate bundle from Mozilla

* Sun Aug 28 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0d-3
- Rename threds.3.bz2, conflicts with perl

* Sat Aug 27 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0d-2
- Remove passwd.1.bz2, shadow provides

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0d-1
- Upgrade to 1.0.0d

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0c-1
- Upgrade to 1.0.0c

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0a-1
- Upgrade to 1.0.0a

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0-1
- Initial version
