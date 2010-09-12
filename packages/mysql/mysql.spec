Summary: The MySQL Database
Name: mysql
Version: 5.1.50
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mysql.com
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = fb5982fb73bb2eb0494615352a7510f75114c6d9
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: zlib-devel

%description
MySQL is a relational database management system that runs as a server
providing multi-user access to a number of databases.

%package devel
Summary: Headers and libraries for developing with mysql
Group: Development/Libraries

%description devel
Headers and libraries for developing with mysql

%prep
%setup -q
# we need to filter out a few auto requirements
cat > %{name}-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed -e '/perl(DBI)/d'
EOF
chmod +x %{name}-req
%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req

%build
CFLAGS="-O3 -pipe" \
LDFLAGS="%{LDFLAGS}" \
CXX=gcc \
CXXFLAGS="-O3 -pipe -felide-constructors -fno-exceptions -fno-rtti" \
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --libexecdir=/usr/sbin \
  --localstatedir=/srv/mysql \
  --with-unix-socket-path=/var/run/mysql/mysql.sock \
  --with-extra-charsets=all \
  --enable-assembler \
  --with-ssl=/usr \
  --with-plugins=innobase,myisam,federated
make

%install
make DESTDIR=%{buildroot} install
# Install the LSB bootscript
install -dv %{buildroot}/etc/init.d
sed -i 's@ \$remote_fs@@' %{buildroot}/usr/share/mysql/mysql.server
sed -i -e 's@2 3 4 5@3 4 5@' -e 's@0 1 6@0 1 2 6@' %{buildroot}/usr/share/mysql/mysql.server
install -m0754 %{buildroot}/usr/share/mysql/mysql.server %{buildroot}/etc/init.d/mysql
# Add some links to libmysql for compatibility
cd %{buildroot}/usr/%{_lib} ; ln -vs mysql/libmysqlclient{,_r}.so* .
# Create necessry runtime directories
install -dv %{buildroot}{/srv,/var/run}/mysql
# Compress man pages
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -f %{buildroot}/usr/share/info/dir
# don't need the test or bench items
rm -rf %{buildroot}/usr/{sql-bench,mysql-test}
# Add the default configuration file
install -vm0644 %{buildroot}/usr/share/mysql/my-medium.cnf %{buildroot}/etc/my.cnf
sed -i 's@\(dirname\|touch\)@/usr/bin/&@' %{buildroot}/usr/bin/mysqld_safe 

%post
/usr/bin/install-info /usr/share/info/mysql.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/mysql.info /usr/share/info/dir
/usr/sbin/remove_initd mysql || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/my.cnf
/etc/init.d/mysql
/usr/bin/innochecksum
/usr/bin/msql2mysql
/usr/bin/my_print_defaults
/usr/bin/myisam_ftdump
/usr/bin/myisamchk
/usr/bin/myisamlog
/usr/bin/myisampack
/usr/bin/mysql
/usr/bin/mysql_client_test
/usr/bin/mysql_config
/usr/bin/mysql_convert_table_format
/usr/bin/mysql_find_rows
/usr/bin/mysql_fix_extensions
/usr/bin/mysql_fix_privilege_tables
/usr/bin/mysql_install_db
/usr/bin/mysql_secure_installation
/usr/bin/mysql_setpermission
/usr/bin/mysql_tzinfo_to_sql
/usr/bin/mysql_upgrade
/usr/bin/mysql_waitpid
/usr/bin/mysql_zap
/usr/bin/mysqlaccess
/usr/bin/mysqladmin
/usr/bin/mysqlbinlog
/usr/bin/mysqlbug
/usr/bin/mysqlcheck
/usr/bin/mysqld_multi
/usr/bin/mysqld_safe
/usr/bin/mysqldump
/usr/bin/mysqldumpslow
/usr/bin/mysqlhotcopy
/usr/bin/mysqlimport
/usr/bin/mysqlshow
/usr/bin/mysqlslap
/usr/bin/mysqltest
/usr/bin/perror
/usr/bin/replace
/usr/bin/resolve_stack_dump
/usr/bin/resolveip
/usr/%{_lib}/libmysqlclient.so.16
/usr/%{_lib}/libmysqlclient.so.16.0.0
/usr/%{_lib}/libmysqlclient_r.so.16
/usr/%{_lib}/libmysqlclient_r.so.16.0.0
%dir /usr/%{_lib}/mysql
/usr/%{_lib}/mysql/libmysqlclient.so.16
/usr/%{_lib}/mysql/libmysqlclient.so.16.0.0
/usr/%{_lib}/mysql/libmysqlclient_r.so.16
/usr/%{_lib}/mysql/libmysqlclient_r.so.16.0.0
%dir /usr/%{_lib}/mysql/plugin
/usr/%{_lib}/mysql/plugin/ha_archive.so.0
/usr/%{_lib}/mysql/plugin/ha_archive.so.0.0.0
/usr/%{_lib}/mysql/plugin/ha_blackhole.so.0
/usr/%{_lib}/mysql/plugin/ha_blackhole.so.0.0.0
/usr/%{_lib}/mysql/plugin/ha_example.so.0
/usr/%{_lib}/mysql/plugin/ha_example.so.0.0.0
/usr/%{_lib}/mysql/plugin/ha_innodb_plugin.so.0
/usr/%{_lib}/mysql/plugin/ha_innodb_plugin.so.0.0.0
/usr/%{_lib}/mysql/plugin/libdaemon_example.so.0
/usr/%{_lib}/mysql/plugin/libdaemon_example.so.0.0.0
/usr/%{_lib}/mysql/plugin/mypluglib.so.0
/usr/%{_lib}/mysql/plugin/mypluglib.so.0.0.0
/usr/share/mysql
/usr/share/info/mysql.info
/usr/share/man/man1/*
/usr/share/man/man8/*
/usr/sbin/mysqld
/usr/sbin/mysqlmanager
%defattr(-,mysql,mysql)
%dir /srv/mysql
%dir /var/run/mysql

%files devel
%defattr(-,root,root)
/usr/share/aclocal/mysql.m4
/usr/include/mysql
/usr/%{_lib}/libmysqlclient.so
/usr/%{_lib}/libmysqlclient_r.so
/usr/%{_lib}/mysql/libdbug.a
/usr/%{_lib}/mysql/libheap.a
/usr/%{_lib}/mysql/libmyisam.a
/usr/%{_lib}/mysql/libmyisammrg.a
/usr/%{_lib}/mysql/libmysqlclient.a
/usr/%{_lib}/mysql/libmysqlclient.la
/usr/%{_lib}/mysql/libmysqlclient.so
/usr/%{_lib}/mysql/libmysqlclient_r.a
/usr/%{_lib}/mysql/libmysqlclient_r.la
/usr/%{_lib}/mysql/libmysqlclient_r.so
/usr/%{_lib}/mysql/libmystrings.a
/usr/%{_lib}/mysql/libmysys.a
/usr/%{_lib}/mysql/libvio.a
/usr/%{_lib}/mysql/plugin/ha_archive.a
/usr/%{_lib}/mysql/plugin/ha_archive.la
/usr/%{_lib}/mysql/plugin/ha_archive.so
/usr/%{_lib}/mysql/plugin/ha_blackhole.a
/usr/%{_lib}/mysql/plugin/ha_blackhole.la
/usr/%{_lib}/mysql/plugin/ha_blackhole.so
/usr/%{_lib}/mysql/plugin/ha_example.a
/usr/%{_lib}/mysql/plugin/ha_example.la
/usr/%{_lib}/mysql/plugin/ha_example.so
/usr/%{_lib}/mysql/plugin/ha_innodb_plugin.a
/usr/%{_lib}/mysql/plugin/ha_innodb_plugin.la
/usr/%{_lib}/mysql/plugin/ha_innodb_plugin.so
/usr/%{_lib}/mysql/plugin/libdaemon_example.a
/usr/%{_lib}/mysql/plugin/libdaemon_example.la
/usr/%{_lib}/mysql/plugin/libdaemon_example.so
/usr/%{_lib}/mysql/plugin/mypluglib.a
/usr/%{_lib}/mysql/plugin/mypluglib.la
/usr/%{_lib}/mysql/plugin/mypluglib.so


%changelog
* Thu Sep 02 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.50-1
- Initial version
