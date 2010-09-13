Summary: MongoDB Driver for PHP
Name: php-mongo
Version: 1.0.9
Release: 2
Group: Development/Languages
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pecl.php.net/package/mongo
Source0: http://dev.lightcube.us/sources/%{name}/mongo-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = b4a0d1854faa78b2e8a87d1050495197e0b1cb9e
BuildRequires: php-devel
BuildRequires: autoconf

Requires: php

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
echo 'To activate this module add the following line to /etc/php.ini:
extension=mongo.so'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/php/extensions/mongo.so

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.9-2
- Fix missing dependency on php

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.9-1
- Initial version
