Summary: PHP Hypertext Preprocessor
Name: php
Version: 5.3.6
Release: 3
Group: Development/Languages
License: PHP v3.01
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.php.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/sources/%{name}/%{name}-fpm.init

BuildRequires: digest(sha1:%{SOURCE0}) = 0e0b9b4d9117f22080e2204afa9383469eb0dbbd
BuildRequires: digest(sha1:%{SOURCE1}) = 8e2b3f62bb719db1c29345e0193ce814315e2bb0
BuildRequires: zlib-devel
BuildRequires: libxml2-devel
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: libevent-devel
BuildRequires: libpng-devel
BuildRequires: jpeg-devel
BuildRequires: db-devel
BuildRequires: bzip2-devel
BuildRequires: curl-devel
BuildRequires: gdbm-devel
BuildRequires: ncurses-devel
BuildRequires: httpd-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel

%description
PHP is a widely-used general-purpose scripting language that is especially
suited for Web development and can be embedded into HTML.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%package apache
Summary: PHP Module for Apache Httpd Server
Group: Services
Requires: %{name}

%description apache
PHP Module for Apache Httpd Server

%prep
rm -rf %{name}-%{version}-fpm
%setup -q
cd ..
mv -v %{name}-%{version}{,-fpm}
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --with-config-file-path=/etc \
  --mandir=/usr/share/man \
  --enable-sockets \
  --with-libdir=%{_lib} \
  --enable-calendar \
  --enable-bcmath \
  --with-openssl \
  --with-zlib \
  --with-bz2 \
  --with-db4 \
  --with-curl \
  --enable-pcntl \
  --enable-mbstring \
  --with-gettext \
  --with-pcre-regex=/usr \
  --with-libxml-dir=/usr \
  --with-jpeg-dir=/usr \
  --enable-sqlite-utf8 \
  --with-gdbm \
  --enable-soap \
  --enable-ftp \
  --with-gd \
  --with-mysql=mysqlnd \
  --with-mysqli=mysqlnd \
  --with-mysql-sock=/srv/mysql/mysql.sock \
  --with-apxs2=/usr/sbin/apxs
make
cd ../%{name}-%{version}-fpm
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --with-config-file-path=/etc \
  --mandir=/usr/share/man \
  --with-libdir=%{_lib} \
  --enable-sockets \
  --enable-calendar \
  --enable-bcmath \
  --with-openssl \
  --with-zlib \
  --with-bz2 \
  --with-db4 \
  --with-curl \
  --enable-pcntl \
  --enable-mbstring \
  --with-gettext \
  --with-pcre-regex=/usr \
  --with-libxml-dir=/usr \
  --with-jpeg-dir=/usr \
  --enable-sqlite-utf8 \
  --with-gdbm \
  --enable-soap \
  --enable-ftp \
  --with-gd \
  --with-mysql=mysqlnd \
  --with-mysqli=mysqlnd \
  --with-mysql-sock=/srv/mysql/mysql.sock \
  --enable-fpm
make

%install
install -dv %{buildroot}/etc/apache
echo -e "\nLoadModule dummy_module dummy.so\n" > %{buildroot}/etc/apache/httpd.conf
make INSTALL_ROOT=%{buildroot} install
cd ../%{name}-%{version}-fpm
make INSTALL_ROOT=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/php-fpm
install -v -m644 php.ini-production %{buildroot}/etc/php.ini
install -dv %{buildroot}/usr/%{_lib}/php/extensions
sed -i 's@php/includes"@&\ninclude_path = ".:/usr/%{_lib}/php"@' %{buildroot}/etc/php.ini
sed -i 's@extension_dir = "ext"@&\nextension_dir = /usr/%{_lib}/php/extensions@' %{buildroot}/etc/php.ini
sed -e '/^group =/s@=.*@= nogroup@' -e 's@^;pm\.@pm\.@' \
  %{buildroot}/etc/php-fpm.conf.default > %{buildroot}/etc/php-fpm.conf
rm %{buildroot}/etc/php-fpm.conf.default
rm -rf %{buildroot}/etc/apache
rm -rf %{buildroot}/.{channels,depdb,depdblock,filemap,lock}
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%post apache
echo 'To activate this module, add the following lines to /etc/apache/httpd.conf:
LoadModule php5_module %{_lib}/apache/libphp5.so
AddType application/x-httpd-php .php

You may also what to edit "DirectoryIndex" to include index.php'

%preun
/usr/sbin/remove_initd php-fpm || /bin/true

%files
%defattr(-,root,root)
%config /etc/init.d/php-fpm
%config /etc/pear.conf
%config /etc/php-fpm.conf
%config /etc/php.ini
/usr/bin/pear
/usr/bin/peardev
/usr/bin/pecl
/usr/bin/phar
/usr/bin/phar.phar
/usr/bin/php
/usr/%{_lib}/php
/usr/share/man/man1/php.1.bz2
/usr/share/man/man8/php-fpm.8.bz2
/usr/sbin/php-fpm

%files devel
%defattr(-,root,root)
/usr/bin/php-config
/usr/bin/phpize
/usr/include/php
/usr/%{_lib}/build
/usr/share/man/man1/php-config.1.bz2
/usr/share/man/man1/phpize.1.bz2

%files apache
%defattr(-,root,root)
/usr/%{_lib}/apache/libphp5.so

%changelog
* Fri Dec 24 2011 Fitz Agard <fhagard@lightcubesolutions.com> - 5.3.6-3
- Changed mysql.sock location.

* Thu Aug 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.6-2
- Enable support for FTP

* Mon May 09 2011 Archaic <lc@8bitnet.com> - 5.3.6-1
- Updated package version. Fixed default mysql.sock location. Enabled sockets.

* Mon Feb 21 2011 Fitz Agard <fhagard@lightcubesolutions.com> - 5.3.5-1
- Updating package 

* Sat Oct 02 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.3-2
- Remove readline, add pcntl

* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.3-1
- Initial version
