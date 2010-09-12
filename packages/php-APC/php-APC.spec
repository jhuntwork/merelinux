Summary: Alternative PHP Cache
Name: php-APC
Version: 3.1.4
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pecl.php.net/package/APC
Source0: http://dev.lightcube.us/sources/%{name}/APC-%{version}.tgz

BuildRequires: digest(%{SOURCE0}) = 1f7a58f850e795b0958a3f99ae8c2cc4
BuildRequires: php-devel
BuildRequires: autoconf
BuildRequires: pcre-devel

%description
The Alternative PHP Cache (APC) is a free and open opcode cache for PHP. Its
goal is to provide a free, open, and robust framework for caching and
optimizing PHP intermediate code.

%prep
%setup -q -n APC-%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
phpize
./configure
make
make test

%install
make INSTALL_ROOT=%{buildroot} EXTENSION_DIR=/usr/%{_lib}/php/extensions install
install -m644 apc.php %{buildroot}/usr/%{_lib}/php

%post
echo 'To activate this module add the following line to /etc/php.ini:
extension=apc.so'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/php/apc.php
/usr/%{_lib}/php/extensions/apc.so

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.4-1
- Initial version
