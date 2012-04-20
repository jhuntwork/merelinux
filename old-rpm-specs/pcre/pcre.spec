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
#Patch0: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/pcre/posix.patch
Patch0: posix.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 6264472669d8068338cd32128cd4e9742587c676
BuildRequires: digest(sha1:%{PATCH0})  = ea2dab6648c0ccb43d4e3783932f5e3d87db73a8
#BuildRequires: readline-devel
BuildRequires: zlib-devel

%description
The PCRE library is a set of functions that implement regular expression
pattern matching using the same syntax and semantics as Perl 5.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries

%description devel
Headers and libraries for developing with %{name}

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%patch0 -p1
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
export LDFLAGS="--static"
./configure \
  --prefix='' \
  --disable-shared \
  --enable-static \
  --disable-cpp \
  --enable-utf8 \
  --enable-unicode-properties \
  --enable-pcregrep-libz
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/pcregrep
/bin/pcretest
/share/man/man1/pcregrep.1.bz2
/share/man/man1/pcretest.1.bz2

%files devel
%defattr(-,root,root)
/bin/pcre-config
/include/pcre.h
/include/pcreposix.h
/lib/libpcre.a
/lib/libpcre.la
/lib/libpcreposix.a
/lib/libpcreposix.la
/lib/pkgconfig/libpcre.pc
/lib/pkgconfig/libpcreposix.pc
/share/man/man1/pcre-config.1.bz2
/share/man/man3/*.bz2

%files extras
%defattr(-,root,root)
/share/doc/pcre

%changelog
* Tue Jan 31 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.20-1
- Initial version
