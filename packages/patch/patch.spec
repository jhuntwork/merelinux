Summary: GNU Patch
Name: patch
Version: 2.5.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.gnu.org/projects/patch
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-fixes-1.patch

Requires: base-layout, glibc

%description
Patch allows merging of textual changes

%prep
%setup -q
%patch -p1

%build
./configure --prefix=/usr --mandir=/usr/share/man
make

%install
make prefix=%{buildroot}/usr mandir=%{buildroot}/usr/share/man install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/patch
/usr/share/man/man1/patch.1

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
