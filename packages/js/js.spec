Summary: js
Name: js
Version: 1.8.5
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://developer.mozilla.org/en/SpiderMonkey
Source: http://dev.lightcube.us/sources/%{name}/%{name}185-1.0.0.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 52a01449c48d7a117b35f213d3e4263578d846d6
BuildRequires: nspr-devel
BuildRequires: unzip
BuildRequires: zip
 
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
%setup -q

%build
cd js/src
export CFLAGS="-DJS_C_STRINGS_ARE_UTF8"
export CXXFLAGS="-DJS_C_STRINGS_ARE_UTF8"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-pthreads \
  --with-system-nspr \
  --enable-strip
make %{PMFLAGS}

%install
cd js/src
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/%{_lib}/libmozjs185.so
rm -f %{buildroot}/usr/%{_lib}/libmozjs185.so.1.0
ln -sv libmozjs185.so.1.0 %{buildroot}/usr/%{_lib}/libmozjs185.so
ln -sv libmozjs185.so.1.0.0 %{buildroot}/usr/%{_lib}/libmozjs185.so.1.0

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libmozjs185.so.*

%files devel
%defattr(-,root,root)
/usr/bin/js-config
/usr/include/js
/usr/%{_lib}/libmozjs185.so
/usr/%{_lib}/libmozjs185-1.0.a
/usr/%{_lib}/pkgconfig/mozjs185.pc

%changelog
* Mon Apr 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.5-1
- Upgrade to 1.8.5

* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.0-1
- Initial version
