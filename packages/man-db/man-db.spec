Summary: man-db
Name: man-db
Version: 2.5.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://man-db.nongnu.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = e307ec4c440b82c20c9c20984852046d01426333
BuildRequires: gdbm-devel
BuildRequires: zlib-devel

%description
man-db is an implementation of the standard Unix documentation
system accessed using the man command. It uses a Berkeley DB
database in place of the traditional flat-text whatis databases

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
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
%{compress_man}
%find_lang %{name}
%find_lang %{name}-gnulib
cat %{name}-gnulib.lang >> %{name}.lang

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
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
/usr/share/doc/man-db
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.9-1
- Upgraded to 2.5.9

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.7-1
- Upgraded to 2.5.7

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
