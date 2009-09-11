Summary: GNU Diffutils
Name: diffutils
Version: 2.8.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/diffutils
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-i18n-1.patch

Requires: base-layout, glibc

%description
Utilities for comparing differences between files.

%prep
%setup -q
%patch -p1

%build
touch man/diff.1
./configure --prefix=/usr --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/info/dir
%find_lang %{name}

%post
/usr/bin/install-info %{_infodir}/diff.info %{_infodir}/dir

%preun
/usr/bin/install-info --delete %{_infodir}/diff.info %{_infodir}/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/cmp
/usr/bin/diff
/usr/bin/diff3
/usr/bin/sdiff
/usr/info/diff.info
/usr/share/man/man1/cmp.1
/usr/share/man/man1/diff.1
/usr/share/man/man1/diff3.1
/usr/share/man/man1/sdiff.1

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
