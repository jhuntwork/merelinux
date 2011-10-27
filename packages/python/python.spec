Summary: Python Programming Language
Name: python
Version: 2.7.2
Release: 1
Group: Development/Languages
License: Modified CNRI Open Source License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.python.org
Source0: http://www.python.org/ftp/python/2.7.2/Python-2.7.2.tar.bz2
%define abi 2.7

Obsoletes: Python <= %{version}
BuildRequires: digest(sha1:%{SOURCE0}) = 417bdeea77abfaf1b9257fc6b4a04aaa209f4547
BuildRequires: ncurses-devel
BuildRequires: zlib-devel
BuildRequires: readline-devel
BuildRequires: openssl-devel
BuildRequires: bzip2-devel
Provides: python(abi) = %{abi}
Provides: Python

%description
Python is an interpreted, interactive, object-oriented programming
language.

%package devel
Obsoletes: Python-devel <= %{version}
Summary: The libraries and header files needed for Python extension development.
Requires: %{name} >= %{version}
Group: Development/Libraries
Provides: Python-devel

%description devel
The Python programming language's interpreter can be extended with
dynamically loaded extensions and can be embedded in other programs.
This package contains the header files and libraries needed to do
these types of tasks.

%package test
Summary: Extra tests shipped with Python
Requires: %{name} >= %{version}
Group: Development/Libraries

%description test
Test modules shipped with python, separated to save space.

%prep
%setup -q -n Python-%{version}

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --enable-shared
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
sed -i '/#!/s@/local@@' %{buildroot}/usr/lib/python%{abi}/cgi.py
%if "%{_lib}" != "lib"
  install -dv %{buildroot}/usr/lib64
  mv -v %{buildroot}/usr/lib/pkgconfig %{buildroot}/usr/lib64/
  mv -v %{buildroot}/usr/lib/libpython* %{buildroot}/usr/lib64/
%endif
find %{buildroot}/usr/lib/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name config \
  -not -regex '^.*/test.*' -not -regex '^.*/unittest.*' \
  | sed "s|^%{buildroot}||" >python-files
find %{buildroot}/usr/lib/python%{abi}/config \
  -mindepth 1 -maxdepth 1 -not -name Makefile | sed "s|^%{buildroot}||" >devel-files
find %{buildroot}/usr/include/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name pyconfig.h | sed "s|^%{buildroot}||" >>devel-files
%{compress_man}
%{strip}

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
%dir /usr/lib/python%{abi}/test
/usr/lib/python%{abi}/test/test_support.py*
/usr/lib/python%{abi}/test/__init__.py*
/usr/lib/python%{abi}/unittest
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

%files test
%defattr(-,root,root)
/usr/lib/python%{abi}/test/*
%exclude /usr/lib/python%{abi}/test/test_support.py*
%exclude /usr/lib/python%{abi}/test/__init__.py*

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.2
- Upgrade to 2.7.2
- Remove dependency on sqlite and gdbm
- Optimize for size, separate out test modules
- Rename package to 'python'

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
