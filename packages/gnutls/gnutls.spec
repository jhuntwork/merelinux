Summary: GNU Transport Layer Security Library
Name: gnutls
Version: 2.10.1
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gnutls
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 507ff8ad7c1e042f8ecaa4314f32777e74caf0d3
BuildRequires: libgpg-error-devel
BuildRequires: libgcrypt-devel
BuildRequires: zlib-devel
BuildRequires: readline-devel

%description
GnuTLS is a library which provides a secure layer, over a reliable transport
layer. Currently the GnuTLS library implements the proposed standards by the
IETF's TLS working group.

%package devel
Summary: Headers and libraries for developing with gnutls
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with gnutls

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -f %{buildroot}/usr/share/info/dir
%{find_lang} libgnutls

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/install-info /usr/share/info/gnutls.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/gnutls.info /usr/share/info/dir

%postun
/sbin/ldconfig

%files -f libgnutls.lang
%defattr(-,root,root)
/usr/bin/certtool
/usr/bin/gnutls-cli
/usr/bin/gnutls-cli-debug
/usr/bin/gnutls-serv
/usr/bin/psktool
/usr/bin/srptool
/usr/%{_lib}/*.so.*
/usr/share/info/gnutls-certificate-user-use-case.png
/usr/share/info/gnutls-client-server-use-case.png
/usr/share/info/gnutls-extensions_st.png
/usr/share/info/gnutls-handshake-sequence.png
/usr/share/info/gnutls-handshake-state.png
/usr/share/info/gnutls-internals.png
/usr/share/info/gnutls-layers.png
/usr/share/info/gnutls-logo.png
/usr/share/info/gnutls-mod_auth_st.png
/usr/share/info/gnutls-objects.png
/usr/share/info/gnutls-pgp.png
/usr/share/info/gnutls-x509.png
/usr/share/info/gnutls.info
/usr/share/info/gnutls.info-1
/usr/share/info/gnutls.info-2
/usr/share/info/gnutls.info-3
/usr/share/man/man1/*

%files devel
%defattr(-,root,root)
/usr/%{_lib}/*.a
/usr/%{_lib}/*.la
/usr/%{_lib}/*.so
/usr/include/gnutls
/usr/%{_lib}/pkgconfig/gnutls-extra.pc
/usr/%{_lib}/pkgconfig/gnutls.pc
/usr/share/man/man3/*

%changelog
* Thu Sep 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.10.1-1
- Initial version
