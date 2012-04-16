Summary: The Berkeley Database
Name: db
Version: 5.1.19
Release: 1
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
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
cd build_unix
../dist/configure \
  --prefix='' \
  --enable-compat185 \
  --enable-dbm \
  --enable-static \
  --enable-shared \
  --with-crytography=yes
make %{PMFLAGS}

%install
cd build_unix
make docdir=/share/doc/%{name}-%{version} DESTDIR=%{buildroot} install
# rpm expects there to be a db51 directory for headers
install -dv %{buildroot}/include/db51
for i in db.h db_185.h db_cxx.h ; do
    ln -s ../$i %{buildroot}/include/db51/
done
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/db_archive
/bin/db_checkpoint
/bin/db_deadlock
/bin/db_dump
/bin/db_hotbackup
/bin/db_load
/bin/db_log_verify
/bin/db_printlog
/bin/db_recover
/bin/db_replicate
/bin/db_stat
/bin/db_upgrade
/bin/db_verify
/lib/libdb-5.1.so

%files devel
%defattr(-,root,root)
/lib/libdb-5.1.a
/lib/libdb-5.1.la
/lib/libdb-5.so
/lib/libdb.a
/lib/libdb.so
/include/db.h
/include/db_cxx.h
/include/db_185.h
/include/db51
/share/doc/%{name}-%{version}

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.19-1
- Initial version
