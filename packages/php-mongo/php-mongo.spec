Summary: MongoDB Driver for PHP
Name: php-mongo
Version: 1.0.9
Release: 1
Group: Development/Languages
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pecl.php.net/package/mongo
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/mongo-%{version}.tgz

Requires: php
BuildRequires: digest(%{SOURCE0}) = 99646026a03e61d5e33fbe1ee87e7f9b
BuildRequires: php-devel
BuildRequires: autoconf

%description

%prep
%setup -q -n mongo-%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
phpize
./configure
make
make test

%install
make INSTALL_ROOT=%{buildroot} EXTENSION_DIR=/usr/%{_lib}/php/extensions install

%post
/bin/sed -i 's@^\[PHP\]$@&\nextension=mongo.so@' /etc/php.ini

%postun
/bin/sed -i '/^extension=mongo.so/d' /etc/php.ini

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/php/extensions/mongo.so

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.9-1
- Initial version
