Summary: GNU Bison
Name: bison
Version: 2.5
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bison
Source0: http://ftp.gnu.org/gnu/bison/bison-2.5.tar.bz2

Requires: m4
BuildRequires: digest(sha1:%{SOURCE0}) = 907319624fe4f4c5f9e2c3e23601041ac636ae31

%description
Bison is a general purpose parser generator.

%prep
%setup -q
%{config_musl}
sed -i '/elif 0/s@0@defined SLOW_BUT_NO_HACKS@' lib/fseterr.c

%build
export CFLAGS='-D_GNU_FLAGS -DSLOW_BUT_NO_HACKS -Os'
./configure \
  --prefix=''
make %{PMFLAGS}
#make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
rm %{buildroot}/lib/charset.alias
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/bison
/bin/yacc
/lib/liby.a
/share/aclocal/bison-i18n.m4
/share/bison
/share/man/man1/bison.1.bz2
/share/man/man1/yacc.1.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5-1
- Initial version
