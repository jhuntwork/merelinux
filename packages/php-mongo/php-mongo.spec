Summary: MongoDB Driver for PHP
Name: php-mongo
Version: 1.1.4
Release: 1
Group: Development/Languages
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pecl.php.net/package/mongo
Source0: http://dev.lightcube.us/sources/%{name}/mongo-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = dd3356570dab7cd91e660664ef4ab81601f1208a
BuildRequires: php-devel
BuildRequires: autoconf

Requires: php

%description
This package provides an interface for communicating with the MongoDB database in PHP.

%prep
%setup -q -n mongo-%{version}

%build
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
* Sun Sep 12 2010 Fitz Agard <fhagard@lightcubesolutions.com> - 1.1.4-1
- Updating to 1.1.4

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.9-2
- Fix missing dependency on php

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.9-1
- Initial version
