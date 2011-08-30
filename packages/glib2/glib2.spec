Summary: GLib
Name: glib2
Version: 2.28.6
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gtk.org
Source: http://dev.lightcube.us/sources/%{name}/glib-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 51996339c823cf36ba28c774c4afad933d5f5744
BuildRequires: zlib-devel
BuildRequires: pcre-devel

%description
GLib is a low-level core library that forms the basis of GTK+. It provides data
structure handling for C, portability wrappers and interfaces for such run-time
functionality as an event loop, threads, dynamic loading and an object system.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q -n glib-%{version}

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --with-pcre=system
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/gtk-doc
rm -rf %{buildroot}/etc
rm -rf %{buildroot}/usr/share/locale/en@shaw
%{compress_man}
%find_lang glib20

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f glib20.lang
%defattr(-,root,root
/usr/bin/gdbus
/usr/bin/gio-querymodules
/usr/bin/glib-compile-schemas
/usr/bin/glib-genmarshal
/usr/bin/glib-gettextize
/usr/bin/glib-mkenums
/usr/bin/gobject-query
/usr/bin/gsettings
/usr/bin/gtester
/usr/bin/gtester-report
/usr/%{_lib}/libgio-2.0.so.*
/usr/%{_lib}/libglib-2.0.so.*
/usr/%{_lib}/libgmodule-2.0.so.*
/usr/%{_lib}/libgobject-2.0.so.*
/usr/%{_lib}/libgthread-2.0.so.*
/usr/share/glib-2.0
/usr/share/man/man1/gdbus.1.bz2
/usr/share/man/man1/gio-querymodules.1.bz2
/usr/share/man/man1/glib-compile-schemas.1.bz2
/usr/share/man/man1/glib-genmarshal.1.bz2
/usr/share/man/man1/glib-gettextize.1.bz2
/usr/share/man/man1/glib-mkenums.1.bz2
/usr/share/man/man1/gobject-query.1.bz2
/usr/share/man/man1/gsettings.1.bz2
/usr/share/man/man1/gtester-report.1.bz2
/usr/share/man/man1/gtester.1.bz2

%files devel
%defattr(-,root,root)
/usr/include/gio-unix-2.0
/usr/%{_lib}/glib-2.0
/usr/%{_lib}/libgio-2.0.la
/usr/%{_lib}/libgio-2.0.so
/usr/%{_lib}/libglib-2.0.la
/usr/%{_lib}/libglib-2.0.so
/usr/%{_lib}/libgmodule-2.0.la
/usr/%{_lib}/libgmodule-2.0.so
/usr/%{_lib}/libgobject-2.0.la
/usr/%{_lib}/libgobject-2.0.so
/usr/%{_lib}/libgthread-2.0.la
/usr/%{_lib}/libgthread-2.0.so
/usr/%{_lib}/pkgconfig/gio-2.0.pc
/usr/%{_lib}/pkgconfig/gio-unix-2.0.pc
/usr/%{_lib}/pkgconfig/glib-2.0.pc
/usr/%{_lib}/pkgconfig/gmodule-2.0.pc
/usr/%{_lib}/pkgconfig/gmodule-export-2.0.pc
/usr/%{_lib}/pkgconfig/gmodule-no-export-2.0.pc
/usr/%{_lib}/pkgconfig/gobject-2.0.pc
/usr/%{_lib}/pkgconfig/gthread-2.0.pc
/usr/share/aclocal/glib-2.0.m4
/usr/share/aclocal/glib-gettext.m4
/usr/share/aclocal/gsettings.m4
/usr/share/gdb
/usr/include/glib-2.0

%changelog
* Fri Apr 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.28.6-1
- Initial version
