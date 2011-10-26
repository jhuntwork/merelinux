Summary: man-db
Name: man-db
Version: 2.6.0.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://man-db.nongnu.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: https://raw.github.com/jhuntwork/LightCube-OS/730e7e214cb0fcef1b4f9611e33162e620570852/packages/man-db/flock.h.patch

Requires: groff
BuildRequires: digest(sha1:%{SOURCE0}) = 864e79e9369f993bfce0934132d41f29a687a6f4
BuildRequires: digest(sha1:%{PATCH0})  = 93d2affc08e75ad06c79a2344423ec6aee8311e9
BuildRequires: db-devel
BuildRequires: flex
BuildRequires: less
BuildRequires: libpipeline-devel
BuildRequires: util-linux
BuildRequires: zlib-devel

%description
man-db is an implementation of the standard Unix documentation
system accessed using the man command. It uses a Berkeley DB
database in place of the traditional flat-text whatis databases

%prep
%setup -q
%patch0 -p1

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --with-db=db5 \
  --disable-silent-rules \
  --disable-setuid
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/man/{de,es,fr,it,ja}
%{compress_man}
%find_lang %{name}
%find_lang %{name}-gnulib
%{strip}
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
* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.0.2-1
- Upgrade to 2.6.0.2
- Use Berkeley DB instead of gdbm, since db is part of the base system

* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.9-2
- Rebuild with groff dependency, fix broken rpm package.

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.9-1
- Upgraded to 2.5.9

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.7-1
- Upgraded to 2.5.7

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
