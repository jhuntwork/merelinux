Summary: The Expat XML Parser
Name: expat
Version: 2.0.1
Release: 3
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://expat.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 663548c37b996082db1f2f2c32af060d7aa15c2d

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
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/xmlwf
/usr/%{_lib}/libexpat.so.*
/usr/share/man/man1/xmlwf.1.bz2

%files devel
%defattr(-,root,root)
/usr/include/expat.h
/usr/include/expat_external.h
/usr/%{_lib}/libexpat.a
/usr/%{_lib}/libexpat.la
/usr/%{_lib}/libexpat.so

%changelog
* Thu Oct 27 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-3
- Optimize for size

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-2
- Fixes to mandir location

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-1
- Initial version
