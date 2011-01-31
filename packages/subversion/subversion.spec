Summary: Subversion
Name: subversion
Version: 1.6.15
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://subversion.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = b6fadf944a94b86f989f07bc2d781be41df017bf
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: neon-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: expat-devel
BuildRequires: Python-devel
BuildRequires: httpd-devel
BuildRequires: sqlite-devel
BuildRequires: db-devel

%description
Subversion is an open source version control system.

%package devel
Summary: Headers and libraries for developing with Subversion
Group: Development/Libraries
Requires: %{name}, %{name}-python, %{name}-perl

%description devel
Headers and libraries for developing with Subversion

%package python
Summary: Subversion Python Bindings
Group: Development/Libraries
Requires: %{name}, Python

%description python
Subversion Python Bindings

%package perl
Summary: Subversion Perl Bindings
Group: Development/Libraries
Requires: %{name}, perl

%description perl
Subversion Perl Bindings

%package apache
Summary: mod_dav_svn and mod_authz_svn for Apache HTTP Server
Group: Services
Requires: %{name}, httpd

%description apache
Modules for using Subversion with Apache HTTP Server

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
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
make swig-pl

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} install-swig-py
make DESTDIR=%{buildroot} install-swig-pl
%{compress_man}
rm -v %{buildroot}/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
install -dv %{buildroot}/usr/lib/python2.7/site-packages
mv -v %{buildroot}/usr/%{_lib}/svn-python/* %{buildroot}/usr/lib/python2.7/site-packages
rm -rf %{buildroot}/usr/%{_lib}/svn-python
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post apache
echo 'To activate this module, add the following lines to /etc/apache/httpd.conf:
LoadModule dav_svn_module %{_lib}/apache/mod_dav_svn.so
LoadModule authz_svn_module %{_lib}/apache/mod_authz_svn.so'

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
/usr/share/man/man1/svn.1.bz2
/usr/share/man/man1/svnadmin.1.bz2
/usr/share/man/man1/svndumpfilter.1.bz2
/usr/share/man/man1/svnlook.1.bz2
/usr/share/man/man1/svnsync.1.bz2
/usr/share/man/man1/svnversion.1.bz2
/usr/share/man/man5/svnserve.conf.5.bz2
/usr/share/man/man8/svnserve.8.bz2

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
/usr/%{_lib}/libsvn_swig_py-1.a
/usr/%{_lib}/libsvn_swig_py-1.la
/usr/%{_lib}/libsvn_swig_py-1.so
/usr/%{_lib}/libsvn_swig_perl-1.a
/usr/%{_lib}/libsvn_swig_perl-1.la
/usr/%{_lib}/libsvn_swig_perl-1.so
/usr/share/man/man3/SVN::Base.3.bz2
/usr/share/man/man3/SVN::Client.3.bz2
/usr/share/man/man3/SVN::Core.3.bz2
/usr/share/man/man3/SVN::Delta.3.bz2
/usr/share/man/man3/SVN::Fs.3.bz2
/usr/share/man/man3/SVN::Ra.3.bz2
/usr/share/man/man3/SVN::Repos.3.bz2
/usr/share/man/man3/SVN::Wc.3.bz2

%files python
%defattr(-,root,root)
/usr/%{_lib}/libsvn_swig_py-1.so.0
/usr/%{_lib}/libsvn_swig_py-1.so.0.0.0
/usr/lib/python2.7/site-packages/svn
/usr/lib/python2.7/site-packages/libsvn

%files perl
%defattr(-,root,root)
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/SVN
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/SVN
/usr/%{_lib}/libsvn_swig_perl-1.so.0
/usr/%{_lib}/libsvn_swig_perl-1.so.0.0.0

%files apache
%defattr(-,root,root)
/usr/%{_lib}/apache/mod_authz_svn.so
/usr/%{_lib}/apache/mod_dav_svn.so

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.15-1
- Upgrade to 1.6.15

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.12-1
- Upgrade to 1.6.12

* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.9-2
- Include Perl Bindings

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.9-1
- Initial version
