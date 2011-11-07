Summary: PCRE - Perl Compatible Regular Expressions
Name: pcre
Version: 8.20
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.pcre.org
Source0: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/pcre-8.20.tar.bz2
Patch0: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/pcre/posix.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 6264472669d8068338cd32128cd4e9742587c676
BuildRequires: digest(sha1:%{PATCH0})  = ea2dab6648c0ccb43d4e3783932f5e3d87db73a8
BuildRequires: bzip2-devel
BuildRequires: readline-devel
BuildRequires: zlib-devel

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
%patch0 -p1

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --enable-utf8 \
  --libdir=/usr/%{_lib} \
  --enable-unicode-properties \
  --enable-pcregrep-libz \
  --enable-pcretest-libreadline \
  --enable-pcregrep-libbz2
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

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
/usr/share/man/man1/pcregrep.1.bz2
/usr/share/man/man1/pcretest.1.bz2

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
/usr/share/man/man1/pcre-config.1.bz2
/usr/share/man/man3/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.20-1
- Upgrade to 8.20
- Optimize for size

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.13-1
- Upgrade to 8.13

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.10-2
- Add patch for pcreposix which avoids duplicate function names from other
  packages

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.10-1
- Upgrade to 8.10

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.02-1
- Initial version
