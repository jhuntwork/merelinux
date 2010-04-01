Summary: man-db
Name: man-db
Version: 2.5.7
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://man-db.nongnu.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, gdbm, groff
BuildRequires: digest(%{SOURCE0}) = eef0d8c8e54894e4e050e2176bb1d88d

%description
man-db is an implementation of the standard Unix documentation
system accessed using the man command. It uses a Berkeley DB
database in place of the traditional flat-text whatis databases

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --disable-setuid \
  --with-browser=/usr/bin/lynx \
  --with-vgrind=/usr/bin/vgrind \
  --with-grap=/usr/bin/grap
make
make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/man/{de,es,fr,it,ja}
rm -rf %{buildroot}/usr/share/doc
%find_lang %{name}
%find_lang %{name}-gnulib
cat %{name}-gnulib.lang >> %{name}.lang

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc manual/man_db.{ps,cat}
/etc/man_db.conf
/usr/bin/apropos
/usr/bin/catman
/usr/bin/lexgrog
/usr/bin/man
/usr/bin/mandb
/usr/bin/manpath
/usr/bin/whatis
/usr/bin/zsoelim
/usr/%{_lib}/man-db
/usr/sbin/accessdb
/usr/share/man/man1/apropos.1
/usr/share/man/man1/lexgrog.1
/usr/share/man/man1/man.1
/usr/share/man/man1/manconv.1
/usr/share/man/man1/manpath.1
/usr/share/man/man1/whatis.1
/usr/share/man/man1/zsoelim.1
/usr/share/man/man5/manpath.5
/usr/share/man/man8/accessdb.8
/usr/share/man/man8/catman.8
/usr/share/man/man8/mandb.8


%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.7-1
- Upgraded to 2.5.7

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
