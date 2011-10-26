Summary: GNU Diffutils
Name: diffutils
Version: 3.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/diffutils
Source0: http://ftp.gnu.org/gnu/diffutils/diffutils-3.2.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = 59b9742e96e2512d4d6f9af7964d71b6ea5a9ef0

%description
Utilities for comparing differences between files.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --mandir=/usr/share/man \
  --infodir=/usr/share/info
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/diffutils.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/diffutils.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/cmp
/usr/bin/diff
/usr/bin/diff3
/usr/bin/sdiff
/usr/share/info/diffutils.info
/usr/share/man/man1/cmp.1.bz2
/usr/share/man/man1/diff.1.bz2
/usr/share/man/man1/diff3.1.bz2
/usr/share/man/man1/sdiff.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.2-1
- Upgrade to 3.2
- Optimize for size

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0-1
- Upgrade to 3.0

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.9-1
- Upgrade to 2.9

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-2
- Use FHS compatible directories for info files

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.1-1
- Initial version
