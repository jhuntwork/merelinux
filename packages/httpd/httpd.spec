Summary: Apache HTTP Server
Name: httpd
Version: 2.2.21
Release: 1
Group: Services
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://httpd.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/httpd/httpd.init

BuildRequires: digest(sha1:%{SOURCE0}) = c02f9b05da9a7e316ff37d9053dc76a57ba51cb4
BuildRequires: digest(sha1:%{SOURCE1}) = ee24aa6c2e35669e22942840b747e4135693762f
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: db-devel
BuildRequires: expat-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: util-linux-devel
BuildRequires: zlib-devel

%description
The Apache HTTP Server is a popular, secure, efficient and extensible
HTTP server for modern operating systems providing HTTP services in sync with
current HTTP standards.

%package devel
Summary: Header files for developing with Apache httpd
Requires: %{name} >= %{version}

%description devel
Header files for developing with Apache httpd

%prep
%setup -q
# Adjust the location of the build directory
sed -i '/installbuilddir/s@:.*@: ${libexecdir}/build@' config.layout

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --bindir=/usr/bin \
  --sbindir=/usr/sbin \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib}/httpd \
  --includedir=/usr/include/httpd \
  --sysconfdir=/etc/httpd \
  --datadir=/srv/httpd \
  --mandir=/usr/share/man \
  --enable-mods-shared=all \
  --enable-so \
  --enable-ssl \
  --with-pcre \
  --with-z \
  --with-apr=/usr \
  --with-apr-util=/usr
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/var/log/httpd
sed -i -e "s/User daemon/User httpd/" \
       -e "s/Group daemon/Group www/" \
    %{buildroot}/etc/httpd/httpd.conf
install -dv %{buildroot}/etc/init.d
install -dv %{buildroot}/usr/share/httpd
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/httpd
mv -v %{buildroot}/etc/httpd/original %{buildroot}/usr/share/httpd/original-configs
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /etc/httpd
%dir /etc/httpd/extra
%config /etc/httpd/extra/httpd-autoindex.conf
%config /etc/httpd/extra/httpd-dav.conf
%config /etc/httpd/extra/httpd-default.conf
%config /etc/httpd/extra/httpd-info.conf
%config /etc/httpd/extra/httpd-languages.conf
%config /etc/httpd/extra/httpd-manual.conf
%config /etc/httpd/extra/httpd-mpm.conf
%config /etc/httpd/extra/httpd-multilang-errordoc.conf
%config /etc/httpd/extra/httpd-ssl.conf
%config /etc/httpd/extra/httpd-userdir.conf
%config /etc/httpd/extra/httpd-vhosts.conf
%config /etc/httpd/httpd.conf
%config /etc/httpd/magic
%config /etc/httpd/mime.types
%config /etc/init.d/httpd
%dir /usr/%{_lib}/httpd
/usr/%{_lib}/httpd/mod_actions.so
/usr/%{_lib}/httpd/mod_alias.so
/usr/%{_lib}/httpd/mod_asis.so
/usr/%{_lib}/httpd/mod_auth_basic.so
/usr/%{_lib}/httpd/mod_auth_digest.so
/usr/%{_lib}/httpd/mod_authn_anon.so
/usr/%{_lib}/httpd/mod_authn_dbd.so
/usr/%{_lib}/httpd/mod_authn_dbm.so
/usr/%{_lib}/httpd/mod_authn_default.so
/usr/%{_lib}/httpd/mod_authn_file.so
/usr/%{_lib}/httpd/mod_authz_dbm.so
/usr/%{_lib}/httpd/mod_authz_default.so
/usr/%{_lib}/httpd/mod_authz_groupfile.so
/usr/%{_lib}/httpd/mod_authz_host.so
/usr/%{_lib}/httpd/mod_authz_owner.so
/usr/%{_lib}/httpd/mod_authz_user.so
/usr/%{_lib}/httpd/mod_autoindex.so
/usr/%{_lib}/httpd/mod_cern_meta.so
/usr/%{_lib}/httpd/mod_cgi.so
/usr/%{_lib}/httpd/mod_dav.so
/usr/%{_lib}/httpd/mod_dav_fs.so
/usr/%{_lib}/httpd/mod_dbd.so
/usr/%{_lib}/httpd/mod_deflate.so
/usr/%{_lib}/httpd/mod_dir.so
/usr/%{_lib}/httpd/mod_dumpio.so
/usr/%{_lib}/httpd/mod_env.so
/usr/%{_lib}/httpd/mod_expires.so
/usr/%{_lib}/httpd/mod_ext_filter.so
/usr/%{_lib}/httpd/mod_filter.so
/usr/%{_lib}/httpd/mod_headers.so
/usr/%{_lib}/httpd/mod_ident.so
/usr/%{_lib}/httpd/mod_imagemap.so
/usr/%{_lib}/httpd/mod_include.so
/usr/%{_lib}/httpd/mod_info.so
/usr/%{_lib}/httpd/mod_log_config.so
/usr/%{_lib}/httpd/mod_log_forensic.so
/usr/%{_lib}/httpd/mod_logio.so
/usr/%{_lib}/httpd/mod_mime.so
/usr/%{_lib}/httpd/mod_mime_magic.so
/usr/%{_lib}/httpd/mod_negotiation.so
/usr/%{_lib}/httpd/mod_reqtimeout.so
/usr/%{_lib}/httpd/mod_rewrite.so
/usr/%{_lib}/httpd/mod_setenvif.so
/usr/%{_lib}/httpd/mod_speling.so
/usr/%{_lib}/httpd/mod_ssl.so
/usr/%{_lib}/httpd/mod_status.so
/usr/%{_lib}/httpd/mod_substitute.so
/usr/%{_lib}/httpd/mod_unique_id.so
/usr/%{_lib}/httpd/mod_userdir.so
/usr/%{_lib}/httpd/mod_usertrack.so
/usr/%{_lib}/httpd/mod_version.so
/usr/%{_lib}/httpd/mod_vhost_alias.so
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
/usr/share/httpd
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
/var/log/httpd
%defattr(-,httpd,www)
/srv/httpd

%files devel
%defattr(-,root,root)
/usr/include/httpd
/usr/%{_lib}/httpd/build
/usr/%{_lib}/httpd/httpd.exp

%changelog
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.21-1
- Upgrade to 2.2.21
- Use a configuration that is more vanilla and consistent with both FHS and 
  similar services in this distributions
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.17-1
- Upgrade to 2.2.17

* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.16-2
- Fix description

* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.16-1
- Upgrade to 2.2.16

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.15-1
- Initial version
