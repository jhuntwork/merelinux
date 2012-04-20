Summary: cpio
Name: cpio
Version: 2.11
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/cpio
Source0: ftp://ftp.gnu.org/gnu/cpio/cpio-2.11.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 6f1934b0079dc1e85ddff89cabdf01adb3a74abb

%description
GNU cpio copies files into or out of a cpio or tar archive.
The archive can be another file on the disk, a magnetic tape, or a pipe.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}

%build
export CFLAGS="-D_GNU_SOURCE -Os -pipe"
./configure \
  --prefix=/usr \
  --libexecdir=/usr/lib/cpio
make V=1 %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/info
rm -f %{buildroot}/usr/lib/charset.alias
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/cpio
/usr/lib/cpio

%files extras
%defattr(-,root,root)
/usr/share/man/man1/cpio.1.bz2
/usr/share/man/man1/mt.1.bz2

%changelog
* Wed Feb 01 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11-1
- Initial version
