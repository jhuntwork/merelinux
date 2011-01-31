Summary: GNU Tape Archiver
Name: tar
Version: 1.25
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/tar
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 0f0c090e51d127cbeffbb9aeeb90db1181d82aed

%description
The Tar program provides the ability to create tar archives,
as well as various other kinds of manipulation.

%prep
%setup -q

%build
FORCE_UNSAFE_CONFIGURE=1 \
./configure \
  --prefix=/usr \
  --bindir=/bin \
  --libexecdir=/usr/sbin
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
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
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.25-1
- Upgrade to 1.25

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.23-1
- Initial version
