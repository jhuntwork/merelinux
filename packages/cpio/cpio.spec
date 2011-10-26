Summary: cpio
Name: cpio
Version: 2.11
Release: 2
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

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libexecdir=/usr/%{_lib}/cpio
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/cpio.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/cpio.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/cpio
/usr/%{_lib}/cpio
/usr/share/info/cpio.info
/usr/share/man/man1/cpio.1.bz2
/usr/share/man/man1/mt.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11-2
- Optimize for size

* Mon Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11-1
- Initial version
