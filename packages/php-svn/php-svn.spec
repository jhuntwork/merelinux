Summary: Subversion Driver for PHP
Name: php-svn
Version: 1.0.0
Release: 1
Group: Development/Languages
License: PHP
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pecl.php.net/package/svn
Source0: http://dev.lightcube.us/sources/%{name}/svn-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = d80a0e5fecc3e639820e507ad270915eecaf7723
BuildRequires: php-devel
BuildRequires: subversion-devel
BuildRequires: autoconf
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: neon-devel
BuildRequires: sqlite-devel
BuildRequires: expat-devel

%description

%prep
%setup -q -n svn-%{version}

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
extension=svn.so'

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/php/extensions/svn.so

%changelog
* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.0-1
- Initial version
