Summary: The Expat XML Parser
Name: expat
Version: 2.0.1
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://expat.sourceforge.net
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = ee8b492592568805593f81f8cdf2a04c

%description
Expat is an XML parser library written in C. It is a
stream-oriented parser in which an application registers handlers
for things the parser might find in the XML document (like start tags).

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib} --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/xmlwf
/usr/%{_lib}/libexpat.so.*
/usr/share/man/man1/xmlwf.1

%files devel
%defattr(-,root,root)
/usr/include/expat.h
/usr/include/expat_external.h
/usr/%{_lib}/libexpat.a
/usr/%{_lib}/libexpat.la
/usr/%{_lib}/libexpat.so

%changelog
* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-2
- Fixes to mandir location

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-1
- Initial version
