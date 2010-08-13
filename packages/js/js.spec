Summary: js
Name: js
Version: 1.8.0
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://developer.mozilla.org/en/SpiderMonkey
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-rc1.tar.gz

Requires: base-layout, glibc, nspr, readline, ncurses
BuildRequires: digest(%{SOURCE0}) = eaad8815dcc66a717ddb87e9724d964e
BuildRequires: nspr-devel, readline-devel, ncurses-devel

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
%setup -q -n %{name}

%build
cd src
make JS_DIST=/usr JS_THREADSAFE=1 BUILD_OPT=1 -f Makefile.ref

%install
cd src
install -dv %{buildroot}/usr/{bin,%{_lib},include/js}
cp Linux_All_OPT.OBJ/libjs.{a,so} %{buildroot}/usr/%{_lib}/
install -vm 0755 Linux_All_OPT.OBJ/{js,jscpucfg,jskwgen} %{buildroot}/usr/bin
cp *.h %{buildroot}/usr/include/js
cp Linux_All_OPT.OBJ/*.h %{buildroot}/usr/include/js
cp *.tbl %{buildroot}/usr/include/js

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/js
/usr/bin/jscpucfg
/usr/bin/jskwgen
/usr/%{_lib}/libjs.so

%files devel
%defattr(-,root,root)
/usr/include/js
/usr/%{_lib}/libjs.a

%changelog
* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.0-1
- Initial version
