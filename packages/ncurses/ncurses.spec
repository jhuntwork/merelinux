Summary: Ncurses Library
Name: ncurses
Version: 5.7
Release: 3
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/ncurses
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = cce05daf61a64501ef6cd8da1f727ec6

%package devel
Summary: Headers and libraries for developing with %{name} 
Group: Development
Requires: %{name}

%description
%{name} is an API for writing text-based user interfaces.

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure --prefix=/usr --mandir=/usr/share/man --with-shared \
 --without-debug --enable-widec --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
mkdir %{buildroot}/%{_lib}
mv %{buildroot}/usr/%{_lib}/libncursesw.so.5* %{buildroot}/%{_lib}
ln -sfv ../../%{_lib}/libncursesw.so.5 %{buildroot}/usr/%{_lib}/libncursesw.so
for lib in curses ncurses form panel menu
do
  rm -vf %{buildroot}/usr/%{_lib}/lib${lib}.so
  echo "INPUT(-l${lib}w)" >%{buildroot}/usr/%{_lib}/lib${lib}.so
  ln -sfv lib${lib}w.a %{buildroot}/usr/%{_lib}/lib${lib}.a
done
rm -vf %{buildroot}/usr/%{_lib}/libcursesw.so
echo "INPUT(-lncursesw)" >%{buildroot}/usr/%{_lib}/libcursesw.so
ln -sfv libncurses.so %{buildroot}/usr/%{_lib}/libcurses.so
ln -sfv libncurses++w.a %{buildroot}/usr/%{_lib}/libncurses++.a
ln -sfv libncursesw.a %{buildroot}/usr/%{_lib}/libcursesw.a
ln -sfv libncurses.a %{buildroot}/usr/%{_lib}/libcurses.a

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/captoinfo
/usr/bin/clear
/usr/bin/infocmp
/usr/bin/infotocap
/usr/bin/reset
/usr/bin/tic
/usr/bin/toe
/usr/bin/tput
/usr/bin/tset
/%{_lib}/libncursesw.so.*
/usr/%{_lib}/libformw.so.*
/usr/%{_lib}/libmenuw.so.*
/usr/%{_lib}/libpanelw.so.*
%ifnarch x86_64
/usr/%{_lib}/terminfo
%endif
/usr/share/man/man1/*
/usr/share/man/man5/term.5
/usr/share/man/man5/terminfo.5
/usr/share/man/man7/term.7
/usr/share/tabset
/usr/share/terminfo/*

%files devel
%defattr(-,root,root)
/usr/bin/ncursesw5-config
/usr/%{_lib}/libcurses.a
/usr/%{_lib}/libcurses.so
/usr/%{_lib}/libcursesw.a
/usr/%{_lib}/libcursesw.so
/usr/%{_lib}/libform.a
/usr/%{_lib}/libform.so
/usr/%{_lib}/libformw.a
/usr/%{_lib}/libformw.so
/usr/%{_lib}/libmenu.a
/usr/%{_lib}/libmenu.so
/usr/%{_lib}/libmenuw.a
/usr/%{_lib}/libmenuw.so
/usr/%{_lib}/libncurses.a
/usr/%{_lib}/libncurses.so
/usr/%{_lib}/libncurses++.a
/usr/%{_lib}/libncurses++w.a
/usr/%{_lib}/libncursesw.a
/usr/%{_lib}/libncursesw.so
/usr/%{_lib}/libpanel.a
/usr/%{_lib}/libpanel.so
/usr/%{_lib}/libpanelw.a
/usr/%{_lib}/libpanelw.so
/usr/include/*.h
/usr/share/man/man3/*

%changelog
* Fri Apr 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.7-3
- Add missing link for libncurses++w.a

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.7-2
- Remove bad location for installed docs

* Sun Jul 26 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
