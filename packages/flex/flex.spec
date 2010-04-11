Summary: The Fast Lexical Analyzer
Name: flex
Version: 2.5.35
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://flex.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-gcc44-1.patch

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 10714e50cea54dc7a227e3eddcd44d57
BuildRequires: digest(%{PATCH0}) = ad9109820534278c6dd0898178c0788f

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
./configure --prefix=/usr --libdir=/usr/%{_lib} --infodir=/usr/share/info --mandir=/usr/share/man
make
make check

%install
make DESTDIR=%{buildroot} install
ln -sv libfl.a %{buildroot}/usr/%{_lib}/libl.a
ln -sv flex.1 %{buildroot}/usr/share/man/man1/lex.1
cat > %{buildroot}/usr/bin/lex << "EOF"
#!/bin/sh
# Begin /usr/bin/lex

exec /usr/bin/flex -l "$@"

# End /usr/bin/lex
EOF
chmod -v 755 %{buildroot}/usr/bin/lex
rm -f %{buildroot}/usr/share/info/dir
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
/usr/share/man/man1/flex.1
/usr/share/man/man1/lex.1
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
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.35-1
- Initial version
