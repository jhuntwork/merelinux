Summary: The GNU Readline Library
Name: readline
Version: 6.1
Release: 2
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tiswww.case.edu/php/chet/readline/rltop.html
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, ncurses
Requires(post): texinfo, bash
BuildRequires: digest(%{SOURCE0}) = fc2f7e714fe792db1ce6ddc4c9fb4ef3
BuildRequires: ncurses-devel

%package devel
Summary: Headers and objects for developing with %{name}
Group: Development
Requires: %{name}

%description
The GNU Readline library provides a set of functions for use by applications
that allow users to edit command lines as they are typed in.

%description devel
Headers and objects for developing with %{name}

%prep
%setup -q

%build
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
sed -i -e 's/0x0600/0x0601/' \
       -e 's/6\.0/6.1/' \
       -e 's/RL_VERSION_MINOR\t0/RL_VERSION_MINOR\t1/' readline.h
./configure --prefix=/usr --libdir=/%{_lib}
make SHLIB_LIBS=-lncurses

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/%{_lib}
mv -v %{buildroot}/%{_lib}/lib{readline,history}.a %{buildroot}/usr/%{_lib}
rm -v %{buildroot}/%{_lib}/lib{readline,history}.so
ln -sfv ../../%{_lib}/libreadline.so.6 %{buildroot}/usr/%{_lib}/libreadline.so
ln -sfv ../../%{_lib}/libhistory.so.6 %{buildroot}/usr/%{_lib}/libhistory.so
rm -f %{buildroot}/usr/share/info/dir

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
/%{_lib}/libhistory.so.6
/%{_lib}/libhistory.so.6.1
/%{_lib}/libreadline.so.6
/%{_lib}/libreadline.so.6.1

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
/usr/share/man/man3/history.3
/usr/share/man/man3/readline.3

%changelog
* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.1-2
- Fixes to build dependencies

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to 6.1

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
