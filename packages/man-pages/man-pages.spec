Summary: Core System Man Pages
Name: man-pages
Version: 3.24
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.kernel.org/doc/man-pages
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout
BuildRequires: digest(%{SOURCE0}) = aca98183e51772ce81e17c78a46bea5d

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
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.24-1
- Upgrade to 3.24

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
