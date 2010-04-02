Summary: The Berkeley Database
Name: db
Version: 4.8.26
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.oracle.com/technology/products/berkeley-db/db
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 3476bac9ec0f3c40729c8a404151d5e3

%package devel
Summary: Libraries and headers for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description
Berkeley DB is a lightweight embeddable database engine.

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q

%build
cd build_unix
../dist/configure --prefix=/usr --enable-compat185 \
  --enable-cxx --libdir=/usr/%{_lib}
make

%install
cd build_unix
make docdir=/usr/share/doc/%{name}-%{version} DESTDIR=%{buildroot} install
find %{buildroot} -name "*.la" -exec rm -vf '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/db_archive
/usr/bin/db_checkpoint
/usr/bin/db_deadlock
/usr/bin/db_dump
/usr/bin/db_hotbackup
/usr/bin/db_load
/usr/bin/db_printlog
/usr/bin/db_recover
/usr/bin/db_sql
/usr/bin/db_stat
/usr/bin/db_upgrade
/usr/bin/db_verify
/usr/%{_lib}/libdb-4.8.a
/usr/%{_lib}/libdb-4.8.so
/usr/%{_lib}/libdb-4.so
/usr/%{_lib}/libdb_cxx-4.8.a
/usr/%{_lib}/libdb_cxx-4.8.so
/usr/%{_lib}/libdb_cxx-4.so

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libdb.a
/usr/%{_lib}/libdb.so
/usr/%{_lib}/libdb_cxx.a
/usr/%{_lib}/libdb_cxx.so
/usr/include/db.h
/usr/include/db_185.h
/usr/include/db_cxx.h
/usr/share/doc/%{name}-%{version}

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.8.26-1
- Upgrade to 4.8.26

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-2
- Use FHS compatible info directories. Move documentation to devel package.

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-1
- Initial version
