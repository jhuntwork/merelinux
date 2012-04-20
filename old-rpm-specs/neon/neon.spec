Summary: neon HTTP and WebDAV client library
Name: neon
Version: 0.29.6
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.webdav.org/neon
Source0: http://www.webdav.org/neon/neon-0.29.6.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ae1109923303f67ed3421157927bc4bc29c58961
BuildRequires: expat-devel
BuildRequires: zlib-devel
BuildRequires: openssl-devel

%description
neon is an HTTP and WebDAV client library, with a C interface.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="-D_GNU_SOURCE -Os -pipe"
./configure \
  --prefix=/ \
  --with-ssl \
  --disable-shared \
  --enable-static
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
# Remove locale messages for now
rm -rf %{buildroot}/share/locale
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
/bin/neon-config
/include/neon
/lib/libneon.a
/lib/libneon.la
/lib/pkgconfig/neon.pc
/share/doc/%{name}-%{version}
/share/man/man1/*.bz2
/share/man/man3/*.bz2

%changelog
* Fri Apr 20 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.29.6-1
- Initial version
