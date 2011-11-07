Summary: The GNU Readline Library
Name: readline
Version: 6.2
Release: 2
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
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/%{_lib}
make %{PMFLAGS} SHLIB_LIBS=-lncurses

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/%{_lib}
mv -v %{buildroot}/%{_lib}/lib{readline,history}.a %{buildroot}/usr/%{_lib}
rm -v %{buildroot}/%{_lib}/lib{readline,history}.so
ln -sfv ../../%{_lib}/libreadline.so.6 %{buildroot}/usr/%{_lib}/libreadline.so
ln -sfv ../../%{_lib}/libhistory.so.6 %{buildroot}/usr/%{_lib}/libhistory.so
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
for i in history readline rluserman
do
  /usr/bin/install-info /usr/share/info/$i.info /usr/share/info/dir
done

%preun devel
for i in history readline rluserman
do
  /usr/bin/install-info --delete /usr/share/info/$i.info /usr/share/info/dir
done

%files
%defattr(-,root,root)
/%{_lib}/libhistory.so.*
/%{_lib}/libreadline.so.*

%files devel
%defattr(-,root,root)
/usr/share/readline
/usr/include/readline
/usr/%{_lib}/libhistory.a
/usr/%{_lib}/libhistory.so
/usr/%{_lib}/libreadline.a
/usr/%{_lib}/libreadline.so
/usr/share/info/history.info
/usr/share/info/readline.info
/usr/share/info/rluserman.info
/usr/share/man/man3/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.2-2
- Optimize for size

* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.2-1
- Upgrade to 6.2

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.1-2
- Fixes to build dependencies

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to 6.1

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
