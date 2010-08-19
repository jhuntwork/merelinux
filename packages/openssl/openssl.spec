Summary: OpenSSL
Name: openssl
Version: 1.0.0a
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-ldflags-1.patch

Requires: base-layout, glibc, zlib
BuildRequires: digest(%{SOURCE0}) = e3873edfffc783624cfbdb65e2249cbd
BuildRequires: digest(%{PATCH0}) = dad1ab082383bddee627a1c3af624b36
BuildRequires: zlib-devel

%description
OpenSSL provides a robust, commercial-grade, full-featured, and Open Source
toolkit implementing the Secure Sockets Layer (SSL v2/v3) and Transport Layer
Security (TLS v1) protocols as well as a full-strength general purpose
cryptography library. 

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%package misc
Summary: Miscellaneous OpenSSL related tools
Group: System Environment/Utilities
Requires: %{name}

%description misc
Miscellaneous OpenSSL related tools

%prep
%setup -q
%patch0 -p1

%build
./config \
  --openssldir=/etc/ssl \
  --prefix=/usr \
  shared zlib-dynamic
make LDFLAGS=%{LDFLAGS} LIBDIR=%{_lib} MANDIR=/usr/share/man

%install
make INSTALL_PREFIX=%{buildroot} LIBDIR=%{_lib} MANDIR=/usr/share/man install
cp -r certs %{buildroot}/etc/ssl

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
/usr/share/man/man1/*
/usr/share/man/man5/config.5
/usr/share/man/man5/x509v3_config.5
/usr/share/man/man7/des_modes.7

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
/usr/share/man/man3/*

%files misc
%defattr(-,root,root)
/etc/ssl/misc

%changelog
* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0a-1
- Upgrade to 1.0.0a

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0-1
- Initial version
