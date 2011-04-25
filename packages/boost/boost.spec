Summary: Boost C++ Libraries
Name: boost
Version: 1.46.1
Release: 1
Group: Development/Tools
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.boost.org
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 3ca6e173ec805e5126868d8a03618e587aa26aef
BuildRequires: zlib-devel
BuildRequires: Python-devel
BuildRequires: bzip2-devel

%description
Boost provides free peer-reviewed portable C++ source libraries.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q -n %{name}_1_46_1

%build
./bootstrap.sh \
  --prefix=/usr \
  --libdir=/usr/%{_lib}

%install
./bjam \
  --prefix=%{buildroot}/usr \
  --libdir=%{buildroot}/usr/%{_lib} \
  install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libboost_*.so.%{version}

%files devel
%defattr(-,root,root)
/usr/include/boost
/usr/%{_lib}/libboost_*.a
/usr/%{_lib}/libboost_*.so

%changelog
* Mon Apr 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.46.1-1
- Upgrade to 1.46.1

* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.43.0-1
- Initial version
