Summary: Gzip compression utility
Name: gzip
Version: 1.4
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gzip
Source0: http://ftp.gnu.org/gnu/gzip/gzip-1.4.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 1d398dac6a7920a7de6e2685fe472a840eb2ce6e

%description
The GNU zip compression utility.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --bindir=/bin
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/bin
rm -v %{buildroot}/bin/uncompress
mv -v %{buildroot}/bin/{gzexe,zcmp,zdiff,zegrep} %{buildroot}/usr/bin
mv -v %{buildroot}/bin/{zfgrep,zforce,zgrep,zless,zmore,znew} %{buildroot}/usr/bin
rm -f %{buildroot}/usr/share/info/dir
ln -sv /bin/gunzip %{buildroot}/usr/bin/uncompress
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/gzip.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/gzip.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/gunzip
/bin/gzip
/bin/zcat
/usr/bin/gzexe
/usr/bin/uncompress
/usr/bin/zcmp
/usr/bin/zdiff
/usr/bin/zegrep
/usr/bin/zfgrep
/usr/bin/zforce
/usr/bin/zgrep
/usr/bin/zless
/usr/bin/zmore
/usr/bin/znew
/usr/share/info/gzip.info
/usr/share/man/man1/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4-3
- Optimize for size

* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4-2
- Change a hard-linked binary to a symbolic link
- Compress man pages

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4-1
- Upgrade to 1.4

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.13-2
- Use FHS compatible info directories

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.13-1
- Upgrade to 1.3.13

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.12-1
- Initial version
