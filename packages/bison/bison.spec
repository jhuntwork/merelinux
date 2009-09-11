Summary: GNU Bison
Name: bison
Version: 2.4.1
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bison
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, m4

%description
%{name} is a general purpose parser generator.

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
echo '#define YYENABLE_NLS 1' >> config.h
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info %{_infodir}/bison.info %{_infodir}/dir

%preun
/usr/bin/install-info --delete %{_infodir}/bison.info %{_infodir}/dir

%files
%defattr(-,root,root)
/usr/bin/bison
/usr/bin/yacc
/usr/%{_lib}/liby.a
/usr/share/aclocal/bison-i18n.m4
/usr/share/bison/README
/usr/share/bison/bison.m4
/usr/share/bison/c++-skel.m4
/usr/share/bison/c++.m4
/usr/share/bison/c-skel.m4
/usr/share/bison/c.m4
/usr/share/bison/glr.c
/usr/share/bison/glr.cc
/usr/share/bison/java-skel.m4
/usr/share/bison/java.m4
/usr/share/bison/lalr1.cc
/usr/share/bison/lalr1.java
/usr/share/bison/location.cc
/usr/share/bison/m4sugar/foreach.m4
/usr/share/bison/m4sugar/m4sugar.m4
/usr/share/bison/xslt/bison.xsl
/usr/share/bison/xslt/xml2dot.xsl
/usr/share/bison/xslt/xml2text.xsl
/usr/share/bison/xslt/xml2xhtml.xsl
/usr/share/bison/yacc.c
/usr/share/info/bison.info
/usr/share/locale/*/LC_MESSAGES/bison-runtime.mo
/usr/share/locale/*/LC_MESSAGES/bison.mo
/usr/share/man/man1/bison.1
/usr/share/man/man1/yacc.1

%changelog
* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
