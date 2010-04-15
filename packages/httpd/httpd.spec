Summary: Apache HTTP Server
Name: httpd
Version: 2.2.15
Release: 1
Group: Services
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://httpd.apache.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/~jhuntwork/sources/blfs-bootscripts/blfs-bootscripts-20090302.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-config-1.patch

Requires: base-layout, glibc, openssl, pcre, apr, apr-util, zlib
BuildRequires: digest(%{SOURCE0}) = 016cec97337eccead2aad6a7c27f2e14
BuildRequires: digest(%{SOURCE1}) = 7ee5363f223235adc54046623ffa77cd
BuildRequires: digest(%{PATCH0}) = e02a3ec5925eb9e111400b9aa229f822
BuildRequires: openssl-devel, pcre-devel, apr-devel, apr-util-devel, zlib-devel

%description
Subversion is an open source version control system.

%package devel
Summary: Header files for developing with Apache httpd
Requires: httpd

%description devel
Header files for developing with Apache httpd

%prep
%setup -q
%patch0 -p1

%build
%ifarch x86_64
sed -i 's@/lib@/%{_lib}@g' config.layout
%endif
./configure \
  --enable-layout=FHS \
  --enable-mods-shared=all \
  --enable-so \
  --enable-ssl \
  --with-pcre \
  --with-z \
  --with-apr=/usr \
  --with-apr-util=/usr
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/var/log/apache
sed -i -e "s/User daemon/User apache/" \
       -e "s/Group daemon/Group apache/" \
    %{buildroot}/etc/apache/httpd.conf
install -dv %{buildroot}/etc/rc.d/init.d
tar -xf %{SOURCE1}
install -m754 blfs-bootscripts-20090302/blfs/init.d/apache \
  %{buildroot}/etc/rc.d/init.d/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/apache
/etc/rc.d/init.d/apache
%dir /usr/%{_lib}/apache
/usr/%{_lib}/apache/mod_actions.so
/usr/%{_lib}/apache/mod_alias.so
/usr/%{_lib}/apache/mod_asis.so
/usr/%{_lib}/apache/mod_auth_basic.so
/usr/%{_lib}/apache/mod_auth_digest.so
/usr/%{_lib}/apache/mod_authn_anon.so
/usr/%{_lib}/apache/mod_authn_dbd.so
/usr/%{_lib}/apache/mod_authn_dbm.so
/usr/%{_lib}/apache/mod_authn_default.so
/usr/%{_lib}/apache/mod_authn_file.so
/usr/%{_lib}/apache/mod_authz_dbm.so
/usr/%{_lib}/apache/mod_authz_default.so
/usr/%{_lib}/apache/mod_authz_groupfile.so
/usr/%{_lib}/apache/mod_authz_host.so
/usr/%{_lib}/apache/mod_authz_owner.so
/usr/%{_lib}/apache/mod_authz_user.so
/usr/%{_lib}/apache/mod_autoindex.so
/usr/%{_lib}/apache/mod_cern_meta.so
/usr/%{_lib}/apache/mod_cgi.so
/usr/%{_lib}/apache/mod_dav.so
/usr/%{_lib}/apache/mod_dav_fs.so
/usr/%{_lib}/apache/mod_dbd.so
/usr/%{_lib}/apache/mod_deflate.so
/usr/%{_lib}/apache/mod_dir.so
/usr/%{_lib}/apache/mod_dumpio.so
/usr/%{_lib}/apache/mod_env.so
/usr/%{_lib}/apache/mod_expires.so
/usr/%{_lib}/apache/mod_ext_filter.so
/usr/%{_lib}/apache/mod_filter.so
/usr/%{_lib}/apache/mod_headers.so
/usr/%{_lib}/apache/mod_ident.so
/usr/%{_lib}/apache/mod_imagemap.so
/usr/%{_lib}/apache/mod_include.so
/usr/%{_lib}/apache/mod_info.so
/usr/%{_lib}/apache/mod_log_config.so
/usr/%{_lib}/apache/mod_log_forensic.so
/usr/%{_lib}/apache/mod_logio.so
/usr/%{_lib}/apache/mod_mime.so
/usr/%{_lib}/apache/mod_mime_magic.so
/usr/%{_lib}/apache/mod_negotiation.so
/usr/%{_lib}/apache/mod_reqtimeout.so
/usr/%{_lib}/apache/mod_rewrite.so
/usr/%{_lib}/apache/mod_setenvif.so
/usr/%{_lib}/apache/mod_speling.so
/usr/%{_lib}/apache/mod_ssl.so
/usr/%{_lib}/apache/mod_status.so
/usr/%{_lib}/apache/mod_substitute.so
/usr/%{_lib}/apache/mod_unique_id.so
/usr/%{_lib}/apache/mod_userdir.so
/usr/%{_lib}/apache/mod_usertrack.so
/usr/%{_lib}/apache/mod_version.so
/usr/%{_lib}/apache/mod_vhost_alias.so
/usr/sbin/ab
/usr/sbin/apachectl
/usr/sbin/apxs
/usr/sbin/checkgid
/usr/sbin/dbmmanage
/usr/sbin/envvars
/usr/sbin/envvars-std
/usr/sbin/htcacheclean
/usr/sbin/htdbm
/usr/sbin/htdigest
/usr/sbin/htpasswd
/usr/sbin/httpd
/usr/sbin/httxt2dbm
/usr/sbin/logresolve
/usr/sbin/rotatelogs
/usr/share/man/man1/dbmmanage.1
/usr/share/man/man1/htdbm.1
/usr/share/man/man1/htdigest.1
/usr/share/man/man1/htpasswd.1
/usr/share/man/man8/ab.8
/usr/share/man/man8/apachectl.8
/usr/share/man/man8/apxs.8
/usr/share/man/man8/htcacheclean.8
/usr/share/man/man8/httpd.8
/usr/share/man/man8/logresolve.8
/usr/share/man/man8/rotatelogs.8
/usr/share/man/man8/suexec.8
/var/log/apache
%defattr(-,apache,apache)
/srv/www

%files devel
%defattr(-,root,root)
/usr/include/apache
/usr/%{_lib}/apache/build
/usr/%{_lib}/apache/httpd.exp

%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.15-1
- Initial version
