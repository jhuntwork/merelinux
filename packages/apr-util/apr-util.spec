Summary: Apache Portable Runtime Utility
Name: apr-util
Version: 1.3.12
Release: 1
Group: System Environment/Libraries
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://apr.apache.org
Source0: http://apache.tradebit.com/pub//apr/apr-util-1.3.12.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 4902165fc5f2f077afbcc7ddf7ebbf61556a1cda
BuildRequires: apr-devel
BuildRequires: db-devel
BuildRequires: expat-devel
BuildRequires: util-linux-devel

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
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-apr=/usr \
  --with-dbm=db4 \
  --with-berkeley-db
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /usr/%{_lib}/apr-util-1
/usr/%{_lib}/libaprutil-1.so.*
/usr/%{_lib}/apr-util-1/apr_dbm_db-1.so

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

%changelog
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.12-1
- Upgrade to 1.3.12
- Remove dependency on sqlite3
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.10-1
- Upgrade to 1.3.10

* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.9-2
- Build against db5 and sqlite

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.9-1
- Initial version
