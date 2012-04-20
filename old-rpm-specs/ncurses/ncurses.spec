Summary: Ncurses Library
Name: ncurses
Version: 5.9
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/ncurses
Source0: http://ftp.gnu.org/gnu/ncurses/ncurses-5.9.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 3e042e5f2c7223bffdaac9646a533b8c758b65b5
BuildRequires: gcc-c++

%description
Ncurses is an API for writing text-based user interfaces.

%package devel
Summary: Headers and libraries for developing with %{name} 
Group: Development
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q
%{config_musl}
# Use GNU sed located at /bin/sed in MKlib_gen.sh
#sed -i '/^[| ]*sed/s@sed@/bin/&@' ncurses/base/MKlib_gen.sh

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --prefix='' \
  --includedir=/include \
  --with-shared \
  --without-debug \
  --mandir=/share/man
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
ln -s libncurses.so %{buildroot}/lib/libcurses.so
ln -s libncurses.a %{buildroot}/lib/libcurses.a
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/captoinfo
/bin/clear
/bin/infocmp
/bin/infotocap
/bin/reset
/bin/tabs
/bin/tic
/bin/toe
/bin/tput
/bin/tset
/lib/libncurses.so.*
/lib/libform.so.*
/lib/libmenu.so.*
/lib/libpanel.so.*
/lib/terminfo
/share/tabset
/share/terminfo/*
/share/man/man1/*.bz2
/share/man/man5/*.bz2
/share/man/man7/*.bz2

%files devel
%defattr(-,root,root)
/bin/ncurses5-config
/lib/libncurses++.a
/lib/libcurses.a
/lib/libcurses.so
/lib/libform.a
/lib/libform.so
/lib/libmenu.a
/lib/libmenu.so
/lib/libncurses.a
/lib/libncurses.so
/lib/libpanel.a
/lib/libpanel.so
/include/*.h
/share/man/man3/*.bz2

%changelog
* Sun Jan 29 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.9-1
- Initial version
