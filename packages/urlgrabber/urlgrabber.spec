Summary: Python File Fetcher
Name: urlgrabber
Version: 3.9.1
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://urlgrabber.baseurl.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

Requires: pycurl
BuildRequires: digest(sha1:%{SOURCE0}) = 937c7ad3177539c337d4010e0175b2c7bd874938
BuildRequires: Python-devel
BuildRequires: pycurl

%description
urlgrabber is a pure python package that drastically simplifies the fetching of
files. It is designed to be used in programs that need common (but not
necessarily simple) url-fetching features.

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
/usr/bin/urlgrabber
/usr/lib/python2.7/site-packages/urlgrabber
/usr/lib/python2.7/site-packages/urlgrabber-%{version}-py2.7.egg-info
/usr/share/doc/urlgrabber-%{version}

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.9.1-1
- Initial version
