Summary: GNU Findutils
Name: findutils
Version: 4.4.2
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/findutils
Source0: http://ftp.gnu.org/gnu/findutils/findutils-4.4.2.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = e8dd88fa2cc58abffd0bfc1eddab9020231bb024

%description
Utilities for searching files in a directory hierarchy.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libexecdir=/usr/%{_lib}/findutils \
  --localstatedir=/var/lib/locate
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
mkdir %{buildroot}/bin
mv -v %{buildroot}/usr/bin/find %{buildroot}/bin
sed -i 's/find:=${BINDIR}/find:=\/bin/' %{buildroot}/usr/bin/updatedb
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/find.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/find-maint.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/find.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/find-maint.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/find
/usr/bin/locate
/usr/bin/oldfind
/usr/bin/updatedb
/usr/bin/xargs
/usr/%{_lib}/findutils
/usr/share/info/find-maint.info
/usr/share/info/find.info
/usr/share/man/man1/find.1.bz2
/usr/share/man/man1/locate.1.bz2
/usr/share/man/man1/updatedb.1.bz2
/usr/share/man/man1/xargs.1.bz2
/usr/share/man/man5/locatedb.5.bz2


%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.2-3
- Optimize for size

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.2-2
- Use FHS compatible info directories

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.2-1
- Initial version
