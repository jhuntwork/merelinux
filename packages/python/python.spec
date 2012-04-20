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
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: zlib-devel
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

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q -n Python-%{version}
sed -i 's/-O3/-Os -g -D_BSD_SOURCE/' `grep -l -r "\-O3" .`
%{config_musl}

%build
export CFLAGS='-g -D_GNU_SOURCE -Os -pipe -Werror=implicit-function-declaration'
export LDFLAGS='-g'
./configure \
  --prefix=/usr \
  --enable-shared \
  --without-pymalloc
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
sed -i '/#!/s@/local@@' %{buildroot}/usr/lib/python%{abi}/cgi.py
find %{buildroot}/usr/lib/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name config \
  -not -regex '^.*/test.*' -not -regex '^.*/unittest.*' \
  | sed "s|^%{buildroot}||" >python-files
find %{buildroot}/usr/lib/python%{abi}/config \
  -mindepth 1 -maxdepth 1 -not -name Makefile | sed "s|^%{buildroot}||" >devel-files
find %{buildroot}/usr/include/python%{abi} \
  -mindepth 1 -maxdepth 1 -not -name pyconfig.h | sed "s|^%{buildroot}||" >>devel-files
%{compress_man}
#%{strip}

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
/usr/lib/libpython2.7.so.1.0

%files -f devel-files devel
%defattr(-,root,root)
/usr/lib/libpython2.7.so
/usr/lib/pkgconfig/python-%{abi}.pc
/usr/lib/pkgconfig/python.pc

%files extras
%defattr(-,root,root)
/usr/lib/python%{abi}/test/*
%exclude /usr/lib/python%{abi}/test/test_support.py*
%exclude /usr/lib/python%{abi}/test/__init__.py*
/usr/share/man/man1/python%{abi}.1.bz2

%changelog
* Tue Jan 31 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.2-1
- Initial version
