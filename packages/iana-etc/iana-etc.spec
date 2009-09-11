Summary: Network protocol and services data
Name: iana-etc
Version: 2.30
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sethwklein.net/iana-etc
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Buildarch: noarch
Requires: base-layout

%description
%{name} provides the /etc/protocols and /etc/services files created from raw data
provided by IANA

%prep
%setup -q

%build
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/protocols
/etc/services

%changelog
* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.30-1
- Initial version
