Summary: The sqlite Database
Name: sqlite
Version: 3.6.23.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.sqlite.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-amalgamation-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = ed585bb3d4e5c643843ebb1e318644ce

%description
SQLite is a in-process library that implements a self-contained, serverless,
zero-configuration, transactional SQL database engine

%package devel
Summary: Libraries and headers for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/sqlite3
/usr/%{_lib}/libsqlite3.so.0
/usr/%{_lib}/libsqlite3.so.0.8.6
/usr/share/man/man1/sqlite3.1

%files devel
%defattr(-,root,root)
/usr/include/sqlite3.h
/usr/include/sqlite3ext.h
/usr/%{_lib}/libsqlite3.a
/usr/%{_lib}/libsqlite3.la
/usr/%{_lib}/libsqlite3.so
/usr/%{_lib}/pkgconfig/sqlite3.pc

%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.6.23.1-1
- Initial version
