Summary: PycURL
Name: pycurl
Version: 7.19.0
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pycurl.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 3fb59eca1461331bb9e9e8d6fe3b23eda961a416
BuildRequires: Python-devel
BuildRequires: curl-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
PycURL is a Python interface to libcurl. PycURL can be used to fetch objects
identified by a URL from a Python program, similar to the urllib Python module.
PycURL is mature, very fast, and supports a lot of features.

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
python ./setup.py build

%install
python ./setup.py install --root=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/curl
/usr/lib/python2.7/site-packages/pycurl-7.19.0-py2.7.egg-info
/usr/lib/python2.7/site-packages/pycurl.so
/usr/share/doc/pycurl

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.19.0-1
- Initial version
