Summary: The Berkeley Database
Name: db
Version: 5.3.15
Release: 1
Group: System Environment/Base
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.oracle.com/technology/products/berkeley-db/db
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 7683b632a01ff3543c379a120809a942ec457738

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
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
export LDFLAGS="--static"
cd build_unix
../dist/configure \
  --prefix='' \
  --enable-compat185 \
  --enable-dbm \
  --enable-sql \
  --enable-sql_codegen \
  --enable-static \
  --disable-shared \
  --with-crytography=yes
make %{PMFLAGS}

%install
cd build_unix
make docdir=/share/doc/%{name}-%{version} DESTDIR=%{buildroot} install
# rpm expects there to be a db53 directory for headers
install -dv %{buildroot}/include/db53
for i in %{buildroot}/include/db*.h ; do
    name=`basename $i`
    ln -s ../$name %{buildroot}/include/db53/
done
for i in %{buildroot}/bin/db* ; do
    name=`basename $i`
    new=`echo $name | sed 's@db@db53@'`
    ln -s $name %{buildroot}/bin/$new
done

%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/db_archive
/bin/db53_archive
/bin/db_checkpoint
/bin/db53_checkpoint
/bin/db_deadlock
/bin/db53_deadlock
/bin/db_dump
/bin/db53_dump
/bin/db_hotbackup
/bin/db53_hotbackup
/bin/db_load
/bin/db53_load
/bin/db_log_verify
/bin/db53_log_verify
/bin/db_printlog
/bin/db53_printlog
/bin/db_recover
/bin/db53_recover
/bin/db_replicate
/bin/db53_replicate
/bin/db_sql_codegen
/bin/db53_sql_codegen
/bin/db_stat
/bin/db53_stat
/bin/db_tuner
/bin/db53_tuner
/bin/db_upgrade
/bin/db53_upgrade
/bin/db_verify
/bin/db53_verify
/bin/dbsql
/bin/db53sql

%files devel
%defattr(-,root,root)
/lib/libdb-5.3.a
/lib/libdb.a
/lib/libdb_sql-5.3.a
/lib/libdb_sql.a
/include/db.h
/include/db_cxx.h
/include/db_185.h
/include/dbsql.h
/include/db53
/share/doc/%{name}-%{version}

%changelog
* Fri Apr 20 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.20-1
- Initial version
