Summary: The eXtensible ARchive format
Name: xar
Version: 1.5.2
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://code.google.com/p/xar
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, libxml2, openssl, zlib, bzip2
BuildRequires: digest(%{SOURCE0}) = 8eabb055d3387b8edc30ecfb08d2e80d
BuildRequires: libxml2-devel, openssl-devel, zlib-devel, bzip2-devel

%description
Xar provides a utility for manipulating files in XAR format.

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
  --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/xar
/usr/%{_lib}/libxar.so.1
/usr/share/man/man1/xar.1

%files devel
%defattr(-,root,root)
/usr/include/xar
/usr/%{_lib}/libxar.a
/usr/%{_lib}/libxar.la
/usr/%{_lib}/libxar.so

%changelog
* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5.2-1
- Initial version
