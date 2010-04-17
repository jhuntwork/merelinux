Summary: Python Programming Language
Name: Python
Version: 2.6.5
Release: 1
Group: Development/Languages
License: Modified CNRI Open Source License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.python.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, ncurses, zlib, readline
BuildRequires:  digest(%{SOURCE0}) = 6bef0417e71a1a1737ccf5750420fdb3
BuildRequires: ncurses-devel, zlib-devel, readline-devel
Provides: python(abi) = 2.6

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
%ifarch x86_64
for file in $(grep "lib" Lib/* -Rl) ; do sed -i 's/"lib"/"lib64"/g' $file; done
sed -i 's@/lib/@/lib64/@' setup.py
for file in $(grep lib\/python Lib/* Modules/* -Rl) ; do sed -i 's@lib/python@lib64/python@g' $file ; done
for file in $(grep "prefix)/lib" * -Rl) ; do sed -i 's@prefix)/lib@&64@g' $file ; done
%endif

%build
./configure --prefix=/usr --enable-shared
make

%install
make DESTDIR=%{buildroot} install
sed -i '/#!/s@/local@@' %{buildroot}/usr/%{_lib}/python2.6/cgi.py
find %{buildroot}/usr/%{_lib}/python2.6 -maxdepth 1 -mindepth 1 -not -name config >libfiles
sed -i 's@%{buildroot}@@' libfiles

%clean
rm -rf %{buildroot}

%files -f libfiles
%defattr(-,root,root)
/usr/bin/2to3
/usr/bin/idle
/usr/bin/pydoc
/usr/bin/python
/usr/bin/python-config
/usr/bin/python2.6
/usr/bin/python2.6-config
/usr/bin/smtpd.py
%dir /usr/%{_lib}/python2.6
/usr/%{_lib}/libpython2.6.so
/usr/%{_lib}/libpython2.6.so.1.0
/usr/share/man/man1/python.1

%files devel
%defattr(-,root,root)
/usr/include/python2.6
/usr/%{_lib}/python2.6/config

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.5-1
- Upgrade to 2.6.5

* Tue Dec 29 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.4-1
- Upgrade to 2.6.4

* Sun Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.3-1
- Upgrade to 2.6.3

* Tue Sep 8 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
