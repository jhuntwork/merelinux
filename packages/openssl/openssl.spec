Summary: OpenSSL
Name: openssl
Version: 1.0.0
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 89eaa86e25b2845f920ec00ae4c864ed

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

%build
./config \
  --openssldir=/etc/ssl \
  --prefix=/usr \
  shared
make LIBDIR=%{_lib} MANDIR=/usr/share/man

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
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0-1
- Initial version
