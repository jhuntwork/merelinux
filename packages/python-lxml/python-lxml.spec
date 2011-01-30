Summary: Python binding for libxml2 and libxslt
Name: python-lxml
Version: 2.2.8
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://codespeak.net/lxml
Source0: http://dev.lightcube.us/sources/python-lxml/lxml-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = 9012ae676160d0d2fff980b07607084e26d53da7
BuildRequires: Python-devel
BuildRequires: libxml2-devel
BuildRequires: libxslt-devel
BuildRequires: zlib-devel

%description
lxml is a Pythonic binding for the libxml2 and libxslt libraries. It is unique
in that it combines the speed and feature completeness of these libraries with
the simplicity of a native Python API, mostly compatible but superior to the
well-known ElementTree API.

%prep
%setup -q -n lxml-%{version}

%build
export LDFLAGS="%{LDFLAGS}"
python ./setup.py build

%install
python ./setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/lxml
/usr/lib/python2.7/site-packages/lxml-2.2.8-py2.7.egg-info

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.613-1
- Initial version
