Summary: The Berkeley Database
Name: db
Version: 5.1.19
Release: 2
Group: System Environment/Base
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.oracle.com/technology/products/berkeley-db/db
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 0c84ed9c6e16857ceb66193bedbb15b05ffbebd0

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
export CFLAGS='-Os -pipe'
cd build_unix
../dist/configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --enable-compat185 \
  --enable-cxx \
  --enable-dbm \
  --enable-sql \
  --enable-sql_codegen \
  --enable-static \
  --enable-shared \
  --with-crytography=yes
make %{PMFLAGS}

%install
cd build_unix
make docdir=/usr/share/doc/%{name}-%{version} DESTDIR=%{buildroot} install
# rpm expects there to be a db51 directory for headers
install -dv %{buildroot}/usr/include/db51
for i in db.h db_185.h db_cxx.h dbsql.h ; do
    ln -sv ../$i %{buildroot}/usr/include/db51/
done
%{strip}

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
/usr/bin/db_log_verify
/usr/bin/db_printlog
/usr/bin/db_recover
/usr/bin/db_replicate
/usr/bin/db_sql_codegen
/usr/bin/dbsql
/usr/bin/db_stat
/usr/bin/db_upgrade
/usr/bin/db_verify
/usr/%{_lib}/libdb-5.1.so
/usr/%{_lib}/libdb_cxx-5.1.so
/usr/%{_lib}/libdb_sql-5.1.so

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libdb-5.1.a
/usr/%{_lib}/libdb-5.1.la
/usr/%{_lib}/libdb-5.so
/usr/%{_lib}/libdb.a
/usr/%{_lib}/libdb.so
/usr/%{_lib}/libdb_cxx-5.1.a
/usr/%{_lib}/libdb_cxx-5.1.la
/usr/%{_lib}/libdb_cxx-5.so
/usr/%{_lib}/libdb_cxx.a
/usr/%{_lib}/libdb_cxx.so
/usr/%{_lib}/libdb_sql-5.1.a
/usr/%{_lib}/libdb_sql-5.1.la
/usr/%{_lib}/libdb_sql-5.so
/usr/%{_lib}/libdb_sql.a
/usr/%{_lib}/libdb_sql.so
/usr/include/db.h
/usr/include/db_185.h
/usr/include/db_cxx.h
/usr/include/dbsql.h
/usr/include/db51
/usr/share/doc/%{name}-%{version}

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.19-2
- Enable dbm
- Optimize for size
- Fix some libs that belonged in devel

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.19-1
- Upgrade to 5.1.19

* Mon Aug 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.0.26-1
- Upgrade to 5.0.26

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.8.26-1
- Upgrade to 4.8.26

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-2
- Use FHS compatible info directories. Move documentation to devel package.

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.7.25-1
- Initial version
