Summary: The GNU Readline Library
Name: readline
Version: 6.0
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tiswww.case.edu/php/chet/readline/rltop.html
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-fixes-1.patch

Requires: base-layout, glibc, ncurses

%package devel
Summary: Headers and objects for developing with %{name}
Group: Development
Requires: glibc-devel, linux-headers, binutils, gcc

%description

%description devel
Headers and objects for developing with %{name}

%prep
%setup -q

%build
sed -i '/MV.*old/d' Makefile.in
sed -i '/{OLDSUFF}/c:' support/shlib-install
patch -Np1 -i %{SOURCE1}
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
  /usr/bin/install-info %{_infodir}/$i.info %{_infodir}/dir
done

%preun devel
for i in history readline rluserman
do
  /usr/bin/install-info --delete %{_infodir}/$i.info %{_infodir}/dir
done

%files
%defattr(-,root,root)
/%{_lib}/libhistory.so.6
/%{_lib}/libhistory.so.6.0
/%{_lib}/libreadline.so.6
/%{_lib}/libreadline.so.6.0

%files devel
%defattr(-,root,root)
%doc doc/*.{ps,pdf,html,dvi}
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
* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
