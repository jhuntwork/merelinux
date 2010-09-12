Summary: Python Programming Language
Name: Python
Version: 2.7
Release: 1
Group: Development/Languages
License: Modified CNRI Open Source License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.python.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
%define abi 2.7

BuildRequires:  digest(%{SOURCE0}) = 0e8c9ec32abf5b732bea7d91b38c3339
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: bzip2-devel
BuildRequires: gdbm-devel
BuildRequires: sqlite-devel
Provides: python(abi) = %{abi}

%description
Python is an interpreted, interactive, object-oriented programming
language.

%package devel
Summary: The libraries and header files needed for Python extension development.
Requires: %{name} = %{version}
Group: Development/Libraries

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --enable-shared
make

%install
make DESTDIR=%{buildroot} install
sed -i '/#!/s@/local@@' %{buildroot}/usr/lib/python%{abi}/cgi.py
%if "%{_lib}" != "lib"
  install -dv %{buildroot}/usr/lib64
  mv -v %{buildroot}/usr/lib/pkgconfig %{buildroot}/usr/lib64/
  mv -v %{buildroot}/usr/lib/libpython* %{buildroot}/usr/lib64/
%endif
find %{buildroot}/usr/lib/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name config | sed "s|^%{buildroot}||" >python-files
find %{buildroot}/usr/lib/python%{abi}/config \
  -mindepth 1 -maxdepth 1 -not -name Makefile | sed "s|^%{buildroot}||" >devel-files
find %{buildroot}/usr/include/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name pyconfig.h | sed "s|^%{buildroot}||" >>devel-files
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files -f python-files
%defattr(-,root,root)
/usr/bin/python
/usr/bin/python-config
/usr/bin/python%{abi}
/usr/bin/python%{abi}-config
/usr/bin/2to3
/usr/bin/idle
/usr/bin/pydoc
/usr/bin/smtpd.py
%dir /usr/include/python%{abi}
/usr/include/python%{abi}/pyconfig.h
%dir /usr/lib/python%{abi}
%dir /usr/lib/python%{abi}/config
/usr/lib/python%{abi}/config/Makefile
/usr/%{_lib}/libpython2.7.so.1.0
/usr/share/man/man1/python%{abi}.1.bz2

%files -f devel-files devel
%defattr(-,root,root)
/usr/%{_lib}/libpython2.7.so
/usr/%{_lib}/pkgconfig/python-%{abi}.pc
/usr/%{_lib}/pkgconfig/python.pc

%changelog
* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7
- Upgrade to 2.7

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.5-1
- Upgrade to 2.6.5

* Tue Dec 29 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.4-1
- Upgrade to 2.6.4

* Sun Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.3-1
- Upgrade to 2.6.3

* Tue Sep 8 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
