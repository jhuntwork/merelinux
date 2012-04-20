Summary: The Fast Lexical Analyzer
Name: flex
Version: 2.5.35
Release: 1
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
sed -i 's/linux-gnu/linux-musl/g' `find . -name config.guess -o -name config.sub`

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man
make %{PMFLAGS}
#make check

%install
make DESTDIR=%{buildroot} install
ln -s libfl.a %{buildroot}/usr/lib/libl.a

cat > %{buildroot}/usr/bin/lex << "EOF"
#!/bin/sh
# Begin /usr/bin/lex

exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF

chmod 0755 %{buildroot}/usr/bin/lex
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
ln -s flex.1.bz2 %{buildroot}/usr/share/man/man1/lex.1.bz2
%{strip}

%clean
rm -rf %{buildroot}

%post extras
/usr/bin/install-info /usr/share/info/flex.info /usr/share/info/dir

%preun extras
/usr/bin/install-info --delete /usr/share/info/flex.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/flex
/usr/bin/lex

%files extras
%defattr(-,root,root)
/usr/share/man/man1/flex.1.bz2
/usr/share/man/man1/lex.1.bz2
/usr/share/info/flex.info
/usr/share/info/flex.info-1
/usr/share/info/flex.info-2

%files devel
%defattr(-,root,root)
/usr/include/FlexLexer.h
/usr/lib/libfl.a
/usr/lib/libfl_pic.a
/usr/lib/libl.a

%changelog
* Thu Jan 26 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.35-1
- Initial version
