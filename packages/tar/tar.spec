Summary: GNU Tape Archiver
Name: tar
Version: 1.26
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/tar
Source0: ftp://ftp.gnu.org/gnu/tar/tar-1.26.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 70f298c3cd997b694864c55e6d8655324c87a0cc

%description
The Tar program provides the ability to create tar archives,
as well as various other kinds of manipulation.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
FORCE_UNSAFE_CONFIGURE=1 \
./configure \
  --prefix=/usr \
  --bindir=/bin \
  --libexecdir=/usr/sbin
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{strip}
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/tar.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/tar.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/tar
/usr/sbin/rmt
/usr/share/info/tar.info
/usr/share/info/tar.info-1
/usr/share/info/tar.info-2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.26-2
- Optimize for size

* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.26-1
- Upgrade to 1.26

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.25-1
- Upgrade to 1.25

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.23-1
- Initial version
