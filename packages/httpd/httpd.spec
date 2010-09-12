Summary: Apache HTTP Server
Name: httpd
Version: 2.2.16
Release: 2
Group: Services
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://httpd.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/sources/%{name}/%{name}.init
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-config-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = ef92f5b3124fe5e9ba6121ea7f4bab8c014068f9
BuildRequires: digest(sha1:%{SOURCE1}) = ee24aa6c2e35669e22942840b747e4135693762f
BuildRequires: digest(sha1:%{PATCH0}) = ec266d894e4f42d813b713af596048879325f22e
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: zlib-devel
BuildRequires: expat-devel
BuildRequires: db-devel

%description
The Apache HTTP Server is a popular, secure, efficient and extensible
HTTP server for modern operating systems providing HTTP services in sync with
current HTTP standards.

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
install -dv %{buildroot}/etc/init.d
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/httpd
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/apache
/etc/init.d/httpd
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
/usr/share/man/man1/dbmmanage.1.bz2
/usr/share/man/man1/htdbm.1.bz2
/usr/share/man/man1/htdigest.1.bz2
/usr/share/man/man1/htpasswd.1.bz2
/usr/share/man/man8/ab.8.bz2
/usr/share/man/man8/apachectl.8.bz2
/usr/share/man/man8/apxs.8.bz2
/usr/share/man/man8/htcacheclean.8.bz2
/usr/share/man/man8/httpd.8.bz2
/usr/share/man/man8/logresolve.8.bz2
/usr/share/man/man8/rotatelogs.8.bz2
/usr/share/man/man8/suexec.8.bz2
/var/log/apache
%defattr(-,apache,apache)
/srv/www

%files devel
%defattr(-,root,root)
/usr/include/apache
/usr/%{_lib}/apache/build
/usr/%{_lib}/apache/httpd.exp

%changelog
* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.16-2
- Fix description

* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.16-1
- Upgrade to 2.2.16

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.15-1
- Initial version
