Summary: BeeCrypt Cryptography Library
Name: beecrypt
Version: 4.2.1
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://beecrypt.sourceforge.net
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 8441c014170823f2dff97e33df55af1e
BuildRequires: Python

%description
BeeCrypt aims to provide a strong and fast cryptography toolkit.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for using %{name} with Python
Group: Development/Librares
Requires: Python

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libbeecrypt.so.*

%files devel
%defattr(-,root,root)
/usr/include/beecrypt
/usr/%{_lib}/libbeecrypt.a
/usr/%{_lib}/libbeecrypt.la
/usr/%{_lib}/libbeecrypt.so

%files python
/usr/%{_lib}/python2.6/site-packages/_bc.a
/usr/%{_lib}/python2.6/site-packages/_bc.la
/usr/%{_lib}/python2.6/site-packages/_bc.so

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-1
- Initial version
