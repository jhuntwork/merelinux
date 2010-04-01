Summary: GNU Diffutils
Name: diffutils
Version: 2.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/diffutils
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = d6bc1bdc874ddb14cfed4d1655a0dbbe

%description
Utilities for comparing differences between files.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --mandir=/usr/share/man \
  --infodir=/usr/share/info
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
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.9-1
- Upgrade to 2.9

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-2
- Use FHS compatible directories for info files

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-1
- Initial version
