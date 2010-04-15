Summary: Apache Portable Runtime Utility
Name: apr-util
Version: 1.3.9
Release: 1
Group: System Environment/Libraries
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://apr.apache.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, apr, expat, db
BuildRequires: digest(%{SOURCE0}) = cc2ec0ba4f01d88375f1170f762518fa
BuildRequires: apr-devel, expat-devel, db-devel

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

%files devel
%defattr(-,root,root)
/usr/bin/apu-1-config
/usr/include/apr-1/apr_anylock.h
/usr/include/apr-1/apr_base64.h
/usr/include/apr-1/apr_buckets.h
/usr/include/apr-1/apr_date.h
/usr/include/apr-1/apr_dbd.h
/usr/include/apr-1/apr_dbm.h
/usr/include/apr-1/apr_hooks.h
/usr/include/apr-1/apr_ldap.h
/usr/include/apr-1/apr_ldap_init.h
/usr/include/apr-1/apr_ldap_option.h
/usr/include/apr-1/apr_ldap_rebind.h
/usr/include/apr-1/apr_ldap_url.h
/usr/include/apr-1/apr_md4.h
/usr/include/apr-1/apr_md5.h
/usr/include/apr-1/apr_memcache.h
/usr/include/apr-1/apr_optional.h
/usr/include/apr-1/apr_optional_hooks.h
/usr/include/apr-1/apr_queue.h
/usr/include/apr-1/apr_reslist.h
/usr/include/apr-1/apr_rmm.h
/usr/include/apr-1/apr_sdbm.h
/usr/include/apr-1/apr_sha1.h
/usr/include/apr-1/apr_strmatch.h
/usr/include/apr-1/apr_thread_pool.h
/usr/include/apr-1/apr_uri.h
/usr/include/apr-1/apr_uuid.h
/usr/include/apr-1/apr_xlate.h
/usr/include/apr-1/apr_xml.h
/usr/include/apr-1/apu.h
/usr/include/apr-1/apu_version.h
/usr/include/apr-1/apu_want.h
/usr/%{_lib}/aprutil.exp
/usr/%{_lib}/libaprutil-1.a
/usr/%{_lib}/libaprutil-1.la
/usr/%{_lib}/libaprutil-1.so
/usr/%{_lib}/pkgconfig/apr-util-1.pc
/usr/%{_lib}/apr-util-1/apr_dbm_db.a
/usr/%{_lib}/apr-util-1/apr_dbm_db.la
/usr/%{_lib}/apr-util-1/apr_dbm_db.so


%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.9-1
- Initial version
