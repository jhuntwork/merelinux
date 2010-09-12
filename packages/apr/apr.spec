Summary: Apache Portable Runtime
Name: apr
Version: 1.4.2
Release: 1
Group: System Environment/Libraries
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://apr.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = d48324efb0280749a5d7ccbb053d68545c568b4b

%description
Apache project core software libraries

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-installbuilddir=/usr/share/apr-1
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libapr-1.so.*

%files devel
%defattr(-,root,root)
/usr/bin/apr-1-config
/usr/include/apr-1
/usr/%{_lib}/apr.exp
/usr/%{_lib}/libapr-1.a
/usr/%{_lib}/libapr-1.la
/usr/%{_lib}/libapr-1.so
/usr/%{_lib}/pkgconfig/apr-1.pc
/usr/share/apr-1

%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.2-1
- Initial version
