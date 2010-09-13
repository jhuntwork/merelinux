Summary: XDebug Extension for PHP
Name: php-xdebug
Version: 2.1.0
Release: 2
Group: Development/Languages
License: Xdebug
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://xdebug.org
Source0: http://dev.lightcube.us/sources/%{name}/xdebug-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = e426e5a4a02e60b34a933c29c98029a0352963be
BuildRequires: php-devel

Requires: php

%description

%prep
%setup -q -n xdebug-%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
phpize
./configure --enable-xdebug
make
make test

%install
make INSTALL_ROOT=%{buildroot} EXTENSION_DIR=/usr/%{_lib}/php/extensions install

%post
echo 'To activate this module add the following line to /etc/php.ini:
zend_extension=/usr/%{_lib}/php/extensions/xdebug.so'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/php/extensions/xdebug.so

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.1.0-2
- Fix output instructions, use --enable-xdebug with configure

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.1.0-1
- Initial version
