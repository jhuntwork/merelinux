Summary: PCRE - Perl Compatible Regular Expressions
Name: pcre
Version: 8.10
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.pcre.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, bzip2, zlib, readline
BuildRequires: digest(%{SOURCE0}) = 780867a700e9d4e4b9cb47aa5453e4b2
BuildRequires: bzip2-devel, zlib-devel, readline-devel

%description
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl 5.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --enable-utf8 \
  --libdir=/usr/%{_lib} \
  --enable-unicode-properties \
  --enable-pcregrep-libz \
  --enable-pcretest-libreadline \
  --enable-pcregrep-libbz2
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/pcregrep
/usr/bin/pcretest
/usr/%{_lib}/libpcre.so.*
/usr/%{_lib}/libpcrecpp.so.*
/usr/%{_lib}/libpcreposix.so.*
/usr/share/doc/pcre
/usr/share/man/man1/pcregrep.1
/usr/share/man/man1/pcretest.1

%files devel
%defattr(-,root,root)
/usr/bin/pcre-config
/usr/include/pcre.h
/usr/include/pcre_scanner.h
/usr/include/pcre_stringpiece.h
/usr/include/pcrecpp.h
/usr/include/pcrecpparg.h
/usr/include/pcreposix.h
/usr/%{_lib}/libpcre.a
/usr/%{_lib}/libpcre.la
/usr/%{_lib}/libpcre.so
/usr/%{_lib}/libpcrecpp.a
/usr/%{_lib}/libpcrecpp.la
/usr/%{_lib}/libpcrecpp.so
/usr/%{_lib}/libpcreposix.a
/usr/%{_lib}/libpcreposix.la
/usr/%{_lib}/libpcreposix.so
/usr/%{_lib}/pkgconfig/libpcre.pc
/usr/%{_lib}/pkgconfig/libpcrecpp.pc
/usr/%{_lib}/pkgconfig/libpcreposix.pc
/usr/share/man/man1/pcre-config.1
/usr/share/man/man3/*

%changelog
* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.10-1
- Upgrade to 8.10

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.02-1
- Initial version
