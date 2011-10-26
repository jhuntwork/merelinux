Summary: GNU Bison
Name: bison
Version: 2.5
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bison
Source0: ftp://ftp.gnu.org/gnu/bison/bison-2.5.tar.bz2

Requires: m4
BuildRequires: digest(sha1:%{SOURCE0}) = 907319624fe4f4c5f9e2c3e23601041ac636ae31

%description
%{name} is a general purpose parser generator.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}
%find_lang %{name}
%find_lang %{name}-runtime
cat %{name}.lang %{name}-runtime.lang > %{name}.files

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/bison.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/bison.info /usr/share/info/dir

%files -f %{name}.files
%defattr(-,root,root)
/usr/bin/bison
/usr/bin/yacc
/usr/%{_lib}/liby.a
/usr/share/aclocal/bison-i18n.m4
/usr/share/bison
/usr/share/info/bison.info
/usr/share/man/man1/bison.1.bz2
/usr/share/man/man1/yacc.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5-1
- Upgrade to 2.5
- Optimize for size

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4.3-1
- Upgrade to 2.4.3

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4.2-1
- Upgrade to 2.4.2

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
