Summary: neon HTTP and WebDAV client library
Name: neon
Version: 0.29.3
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.webdav.org/neon
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, expat, zlib, openssl
BuildRequires: digest(%{SOURCE0}) = ba1015b59c112d44d7797b62fe7bee51
BuildRequires: expat-devel, zlib-devel, openssl-devel

%description
neon is an HTTP and WebDAV client library, with a C interface.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-ssl \
  --enable-shared
make

%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/usr/%{_lib}/libneon.so.*

%files devel
%defattr(-,root,root)
/usr/bin/neon-config
/usr/include/neon
/usr/%{_lib}/libneon.a
/usr/%{_lib}/libneon.la
/usr/%{_lib}/libneon.so
/usr/%{_lib}/pkgconfig/neon.pc
/usr/share/doc/%{name}-%{version}
/usr/share/man/man1/neon-config.1
/usr/share/man/man3/*

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.29.3-1
- Initial version
