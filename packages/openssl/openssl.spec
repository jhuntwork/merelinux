Summary: OpenSSL
Name: openssl
Version: 1.0.0d
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-ldflags-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 32ca934f380a547061ddab7221b1a34e4e07e8d5
BuildRequires: digest(sha1:%{PATCH0})  = 443872eca56c0f5c6f34ec8b07f70a549e830994
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
%{compress_man}

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
* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0d-1
- Upgrade to 1.0.0d

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0c-1
- Upgrade to 1.0.0c

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0a-1
- Upgrade to 1.0.0a

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0-1
- Initial version
