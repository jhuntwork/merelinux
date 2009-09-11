Summary: Core System Man Pages
Name: man-pages
Version: 3.21
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.kernel.org/doc/man-pages
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout

%description
Provides core system man pages.

%prep
%setup -q 

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -type f > files
sed -i 's@^%{buildroot}@@' files

%clean
rm -rf %{buildroot}

%files -f files
%defattr(-,root,root)

%changelog
* Sat Jul 18 2009 Jeremy Huntwork [jhuntwork at lightcube dot us]
- Initial version
