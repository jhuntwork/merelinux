Summary: js
Name: js
Version: 1.7.0
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://developer.mozilla.org/en/SpiderMonkey
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

Obsoletes: js-1.8.5
BuildRequires: digest(sha1:%{SOURCE0}) = 1a99e8e10cb6600a03ea98895583a8ed42136d1f
 
%description
SpiderMonkey is Gecko's JavaScript engine written in C. It is used in various
Mozilla products, including Firefox, and is available under MPL/GPL/LGPL
tri-license.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q -n js

%build
cd src
export CFLAGS="-DJS_C_STRINGS_ARE_UTF8 -Os -pipe"
export CXXFLAGS="-DJS_C_STRINGS_ARE_UTF8 -Os -pipe"
# Can't handle ${PMFLAGS}
make -f Makefile.ref

%install
cd src
make JS_DIST=%{buildroot}/usr -f Makefile.ref export
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/js
/usr/%{_lib}/libjs.so

%files devel
%defattr(-,root,root)
/usr/include/*
/usr/%{_lib}/libjs.a

%changelog
* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.0-2
- Optimize for size

* Tue Oct 04 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.0-1
- Revert to 1.7.0

* Mon Apr 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.5-1
- Upgrade to 1.8.5

* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.0-1
- Initial version
