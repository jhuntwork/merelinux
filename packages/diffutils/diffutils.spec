Summary: GNU Diffutils
Name: diffutils
Version: 2.8.1
Release: 2
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
./configure --prefix=/usr --mandir=/usr/share/man --infodir=/usr/share/info
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/diff.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/diff.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/cmp
/usr/bin/diff
/usr/bin/diff3
/usr/bin/sdiff
/usr/share/info/diff.info
/usr/share/man/man1/cmp.1
/usr/share/man/man1/diff.1
/usr/share/man/man1/diff3.1
/usr/share/man/man1/sdiff.1

%changelog
* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-2
- Use FHS compatible directories for info files

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-1
- Initial version
