Summary: GNU Patch
Name: patch
Version: 2.6.1
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.gnu.org/projects/patch
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-test_fix-1.patch

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 0818d1763ae0c4281bcdc63cdac0b2c0
BuildRequires: digest(%{PATCH0}) = c51e1a95bfc5310635d05081472c3534

%description
Patch allows merging of textual changes

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=/usr
make
make check

%install
make prefix=%{buildroot}/usr mandir=%{buildroot}/usr/share/man install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/patch
/usr/share/man/man1/patch.1

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-2
- Add in a patch for the testsuite

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-1
- Upgrade to 2.6.1

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
