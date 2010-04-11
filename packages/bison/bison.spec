Summary: GNU Bison
Name: bison
Version: 2.4.2
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bison
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, m4
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 63584004613aaef2d3dca19088eb1654

%description
%{name} is a general purpose parser generator.

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
echo '#define YYENABLE_NLS 1' >> lib/config.h
make
#make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
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
/usr/share/man/man1/bison.1
/usr/share/man/man1/yacc.1

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4.2-1
- Upgrade to 2.4.2

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
