Summary: PHP Hypertext Preprocessor
Name: php
Version: 5.3.3
Release: 1
Group: Development/Languages
License: PHP v3.01
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.php.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-fpm.init

BuildRequires: digest(%{SOURCE0}) = 21ceeeb232813c10283a5ca1b4c87b48
BuildRequires: digest(%{SOURCE1}) = a86058855a9c41baa26e019e6528be69
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
BuildRequires: readline-devel
BuildRequires: ncurses-devel

%description
PHP is a widely-used general-purpose scripting language that is especially
suited for Web development and can be embedded into HTML.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --with-config-file-path=/etc \
  --mandir=/usr/share/man \
  --with-libdir=%{_lib} \
  --enable-calendar \
  --enable-bcmath \
  --with-openssl \
  --with-zlib \
  --with-bz2 \
  --with-db4 \
  --with-curl \
  --with-readline \
  --enable-mbstring \
  --with-gettext \
  --with-pcre-regex=/usr \
  --with-libxml-dir=/usr \
  --with-jpeg-dir=/usr \
  --enable-sqlite-utf8 \
  --with-gdbm \
  --enable-fpm \
  --enable-soap \
  --with-gd
make

%install
make INSTALL_ROOT=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/php-fpm
install -v -m644 php.ini-production %{buildroot}/etc/php.ini
install -dv %{buildroot}/usr/%{_lib}/php/extensions
sed -i 's@php/includes"@&\ninclude_path = ".:/usr/%{_lib}/php"@' %{buildroot}/etc/php.ini
sed -i 's@extension_dir = "ext"@&\nextension_dir = /usr/%{_lib}/php/extensions@' %{buildroot}/etc/php.ini
sed -i -e '/^group =/s@=.*@= nogroup@' -e 's@^;pm\.@pm\.@' %{buildroot}/etc/php-fpm.conf.default
rm -rf %{buildroot}/.{channels,depdb,depdblock,filemap,lock}

%clean
rm -rf %{buildroot}

%preun
/usr/sbin/remove_initd php-fpm || /bin/true

%files
%defattr(-,root,root)
/etc/init.d/php-fpm
/etc/pear.conf
/etc/php-fpm.conf.default
/etc/php.ini
/usr/bin/pear
/usr/bin/peardev
/usr/bin/pecl
/usr/bin/phar
/usr/bin/phar.phar
/usr/bin/php
/usr/%{_lib}/php
/usr/share/man/man1/php-fpm.1
/usr/share/man/man1/php.1
/usr/sbin/php-fpm

%files devel
%defattr(-,root,root)
/usr/bin/php-config
/usr/bin/phpize
/usr/include/php
/usr/%{_lib}/build
/usr/share/man/man1/php-config.1
/usr/share/man/man1/phpize.1

%changelog
* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.3-1
- Initial version
