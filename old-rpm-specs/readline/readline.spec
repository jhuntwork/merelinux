Summary: The GNU Readline Library
Name: readline
Version: 6.2
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tiswww.case.edu/php/chet/readline/rltop.html
Source0: http://ftp.gnu.org/gnu/readline/readline-6.2.tar.gz
Patch0: http://ftp.gnu.org/gnu/readline/readline-6.2-patches/readline62-001

BuildRequires: digest(sha1:%{SOURCE0}) = a9761cd9c3da485eb354175fcc2fe35856bc43ac
BuildRequires: digest(sha1:%{PATCH0})  = 7d264c281f3b43e1c07c020b1785631411ce039e
BuildRequires: ncurses-devel

%package devel
Summary: Headers and objects for developing with %{name}
Group: Development
Requires: %{name} >= %{version}

%description
The GNU Readline library provides a set of functions for use by applications
that allow users to edit command lines as they are typed in.

%description devel
Headers and objects for developing with %{name}

%prep
%setup -q
%patch0 -p0
%{config_musl}
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --prefix=''
make %{PMFLAGS} SHLIB_LIBS=-lncurses

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/lib/libhistory.so.*
/lib/libreadline.so.*

%files devel
%defattr(-,root,root)
/share/readline
/include/readline
/lib/libhistory.a
/lib/libhistory.so
/lib/libreadline.a
/lib/libreadline.so
/share/man/man3/*.bz2

%changelog
* Mon Jan 30 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.2-1
- Initial version
