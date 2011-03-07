Summary: Apache Portable Runtime Utility
Name: apr-util
Version: 1.3.10
Release: 1
Group: System Environment/Libraries
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://apr.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 9a720cf77f1d0fdc5b0f6ce6d656cc864d7d4833
BuildRequires: apr-devel
BuildRequires: expat-devel
BuildRequires: db-devel
BuildRequires: sqlite-devel

%description
A companion library to Apache Portable Runtime

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-apr=/usr \
  --with-dbm=db4 \
  --with-berkeley-db
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /usr/%{_lib}/apr-util-1
/usr/%{_lib}/libaprutil-1.so.*
/usr/%{_lib}/apr-util-1/apr_dbm_db-1.so
/usr/%{_lib}/apr-util-1/apr_dbd_sqlite3-1.so

%files devel
%defattr(-,root,root)
/usr/bin/apu-1-config
/usr/include/apr-1/*
/usr/%{_lib}/aprutil.exp
/usr/%{_lib}/libaprutil-1.a
/usr/%{_lib}/libaprutil-1.la
/usr/%{_lib}/libaprutil-1.so
/usr/%{_lib}/pkgconfig/apr-util-1.pc
/usr/%{_lib}/apr-util-1/apr_dbm_db.a
/usr/%{_lib}/apr-util-1/apr_dbm_db.la
/usr/%{_lib}/apr-util-1/apr_dbm_db.so
/usr/%{_lib}/apr-util-1/apr_dbd_sqlite3.a
/usr/%{_lib}/apr-util-1/apr_dbd_sqlite3.la
/usr/%{_lib}/apr-util-1/apr_dbd_sqlite3.so

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.10-1
- Upgrade to 1.3.10

* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.9-2
- Build against db5 and sqlite

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.9-1
- Initial version
