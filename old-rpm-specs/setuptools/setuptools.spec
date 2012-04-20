Summary: setuptools
Name: setuptools
Version: 0.6c11
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pypi.python.org/pypi/setuptools
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 8d1ad6384d358c547c50c60f1bfdb3362c6c4a7d
#BuildRequires: python

%description
Utilities to "Download, build, install, upgrade, and uninstall Python
packages -- easily!"

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/easy_install
/usr/bin/easy_install-2.7
/usr/lib/python2.7/site-packages/*

%changelog
* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.6c11-1
- Initial version
