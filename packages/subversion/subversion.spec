Summary: Subversion
Name: subversion
Version: 1.6.9
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://subversion.apache.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, apr, apr-util, neon, openssl, zlib, sqlite, expat
BuildRequires: digest(%{SOURCE0}) = 9c30a47b1d48664e7afef68bb4834c53
BuildRequires: apr-devel, apr-util-devel, neon-devel, openssl-devel, zlib-devel, sqlite-devel, expat-devel, Python-devel, httpd-devel

%description
Subversion is an open source version control system.

%package devel
Summary: Headers and libraries for developing with Subversion
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with Subversion

%package python
Summary: Subversion Python Bindings
Group: Development/Libraries
Requires: %{name}, Python

%description python
Subversion Python Bindings

%package httpd
Summary: mod_dav_svn and mod_authz_svn for Apache HTTP Server
Group: Services
Requires: %{name}, httpd

%description httpd
Modules for using Subversion with Apache HTTP Server

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-apr=/usr \
  --with-apr-util=/usr \
  --with-neon=/usr \
  --with-sqlite=/usr \
  --with-zlib=/usr \
  --with-editor=/usr/bin/vim \
  --with-ssl
make
make swig-py

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-swig-py
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/svn
/usr/bin/svnadmin
/usr/bin/svndumpfilter
/usr/bin/svnlook
/usr/bin/svnserve
/usr/bin/svnsync
/usr/bin/svnversion
/usr/include/subversion-1
/usr/%{_lib}/libsvn_client-1.so.0
/usr/%{_lib}/libsvn_client-1.so.0.0.0
/usr/%{_lib}/libsvn_delta-1.so.0
/usr/%{_lib}/libsvn_delta-1.so.0.0.0
/usr/%{_lib}/libsvn_diff-1.so.0
/usr/%{_lib}/libsvn_diff-1.so.0.0.0
/usr/%{_lib}/libsvn_fs-1.so.0
/usr/%{_lib}/libsvn_fs-1.so.0.0.0
/usr/%{_lib}/libsvn_fs_base-1.so.0
/usr/%{_lib}/libsvn_fs_base-1.so.0.0.0
/usr/%{_lib}/libsvn_fs_fs-1.so.0
/usr/%{_lib}/libsvn_fs_fs-1.so.0.0.0
/usr/%{_lib}/libsvn_fs_util-1.so.0
/usr/%{_lib}/libsvn_fs_util-1.so.0.0.0
/usr/%{_lib}/libsvn_ra_local-1.so.0
/usr/%{_lib}/libsvn_ra_local-1.so.0.0.0
/usr/%{_lib}/libsvn_ra_neon-1.so.0
/usr/%{_lib}/libsvn_ra_neon-1.so.0.0.0
/usr/%{_lib}/libsvn_ra_svn-1.so.0
/usr/%{_lib}/libsvn_ra_svn-1.so.0.0.0
/usr/%{_lib}/libsvn_ra-1.so.0
/usr/%{_lib}/libsvn_ra-1.so.0.0.0
/usr/%{_lib}/libsvn_repos-1.so.0
/usr/%{_lib}/libsvn_repos-1.so.0.0.0
/usr/%{_lib}/libsvn_subr-1.so.0
/usr/%{_lib}/libsvn_subr-1.so.0.0.0
/usr/%{_lib}/libsvn_wc-1.so.0
/usr/%{_lib}/libsvn_wc-1.so.0.0.0
/usr/share/man/man1/svn.1
/usr/share/man/man1/svnadmin.1
/usr/share/man/man1/svndumpfilter.1
/usr/share/man/man1/svnlook.1
/usr/share/man/man1/svnsync.1
/usr/share/man/man1/svnversion.1
/usr/share/man/man5/svnserve.conf.5
/usr/share/man/man8/svnserve.8

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libsvn_client-1.a
/usr/%{_lib}/libsvn_client-1.la
/usr/%{_lib}/libsvn_client-1.so
/usr/%{_lib}/libsvn_delta-1.a
/usr/%{_lib}/libsvn_delta-1.la
/usr/%{_lib}/libsvn_delta-1.so
/usr/%{_lib}/libsvn_diff-1.a
/usr/%{_lib}/libsvn_diff-1.la
/usr/%{_lib}/libsvn_diff-1.so
/usr/%{_lib}/libsvn_fs-1.a
/usr/%{_lib}/libsvn_fs-1.la
/usr/%{_lib}/libsvn_fs-1.so
/usr/%{_lib}/libsvn_fs_base-1.a
/usr/%{_lib}/libsvn_fs_base-1.la
/usr/%{_lib}/libsvn_fs_base-1.so
/usr/%{_lib}/libsvn_fs_fs-1.a
/usr/%{_lib}/libsvn_fs_fs-1.la
/usr/%{_lib}/libsvn_fs_fs-1.so
/usr/%{_lib}/libsvn_fs_util-1.a
/usr/%{_lib}/libsvn_fs_util-1.la
/usr/%{_lib}/libsvn_fs_util-1.so
/usr/%{_lib}/libsvn_ra-1.a
/usr/%{_lib}/libsvn_ra-1.la
/usr/%{_lib}/libsvn_ra-1.so
/usr/%{_lib}/libsvn_ra_local-1.a
/usr/%{_lib}/libsvn_ra_local-1.la
/usr/%{_lib}/libsvn_ra_local-1.so
/usr/%{_lib}/libsvn_ra_neon-1.a
/usr/%{_lib}/libsvn_ra_neon-1.la
/usr/%{_lib}/libsvn_ra_neon-1.so
/usr/%{_lib}/libsvn_ra_svn-1.a
/usr/%{_lib}/libsvn_ra_svn-1.la
/usr/%{_lib}/libsvn_ra_svn-1.so
/usr/%{_lib}/libsvn_repos-1.a
/usr/%{_lib}/libsvn_repos-1.la
/usr/%{_lib}/libsvn_repos-1.so
/usr/%{_lib}/libsvn_subr-1.a
/usr/%{_lib}/libsvn_subr-1.la
/usr/%{_lib}/libsvn_subr-1.so
/usr/%{_lib}/libsvn_wc-1.a
/usr/%{_lib}/libsvn_wc-1.la
/usr/%{_lib}/libsvn_wc-1.so

%files python
%defattr(-,root,root)
/usr/%{_lib}/libsvn_swig_py-1.so.0
/usr/%{_lib}/libsvn_swig_py-1.so.0.0.0
/usr/%{_lib}/svn-python
/usr/%{_lib}/libsvn_swig_py-1.a
/usr/%{_lib}/libsvn_swig_py-1.la
/usr/%{_lib}/libsvn_swig_py-1.so

%files httpd
%defattr(-,root,root)
/usr/%{_lib}/apache/mod_authz_svn.so
/usr/%{_lib}/apache/mod_dav_svn.so

%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.9-1
- Initial version
