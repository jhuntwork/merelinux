Summary: The Fast Lexical Analyzer
Name: flex
Version: 2.5.35
Release: 2
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://flex.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-gcc44-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = c507095833aaeef2d6502e12638e54bf7ad2f24a
BuildRequires: digest(sha1:%{PATCH0})  = 68ac2b16f2710f9c3bf1e3e90ad833b6f554afe2

%description
Flex is a tool for generating scanners. A scanner, sometimes called a tokenizer,
is a program which recognizes lexical patterns in text.

%package devel
Summary: Provides headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Provides headers and libraries for developing with %{name}

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
ln -sv libfl.a %{buildroot}/usr/%{_lib}/libl.a

cat > %{buildroot}/usr/bin/lex << "EOF"
#!/bin/sh
# Begin /usr/bin/lex

exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF

chmod -v 755 %{buildroot}/usr/bin/lex
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
ln -sv flex.1.bz2 %{buildroot}/usr/share/man/man1/lex.1.bz2
%{strip}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/flex.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/flex.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/flex
/usr/bin/lex
/usr/share/man/man1/flex.1.bz2
/usr/share/man/man1/lex.1.bz2
/usr/share/info/flex.info
/usr/share/info/flex.info-1
/usr/share/info/flex.info-2

%files devel
%defattr(-,root,root)
/usr/include/FlexLexer.h
/usr/%{_lib}/libfl.a
/usr/%{_lib}/libfl_pic.a
/usr/%{_lib}/libl.a

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.35-2
- Optimize for size

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.35-1
- Initial version
