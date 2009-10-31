Summary: The Berkeley Database
Name: db
Version: 4.7.25
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.oracle.com/technology/products/berkeley-db/db
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-upstream_fixes-1.patch

Requires: base-layout, glibc

%package devel
Summary: Libraries and headers for developing with %{name}
Group: Development/Libraries
Requires: glibc-devel linux-headers gcc binutils %{name}

%description
Berkeley DB is a lightweight embeddable database engine.

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q
%patch -p1

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
/usr/bin/db_codegen
/usr/bin/db_deadlock
/usr/bin/db_dump
/usr/bin/db_hotbackup
/usr/bin/db_load
/usr/bin/db_printlog
/usr/bin/db_recover
/usr/bin/db_stat
/usr/bin/db_upgrade
/usr/bin/db_verify
/usr/%{_lib}/libdb-4.7.a
/usr/%{_lib}/libdb-4.7.so
/usr/%{_lib}/libdb-4.so
/usr/%{_lib}/libdb_cxx-4.7.a
/usr/%{_lib}/libdb_cxx-4.7.so
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
* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-2
- Use FHS compatible info directories. Move documentation to devel package.

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-1
- Initial version
