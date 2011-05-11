Summary: Cairo is a 2D graphics library with support for multiple output devices.
Name: cairo
Version: 1.10.2
Release: 1
Group: System Environment/Base
License: LGPLv2.1
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://cairographics.org/
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ccce5ae03f99c505db97c286a0c9a90a926d3c6e
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: pixman-devel
BuildRequires: freetype-devel

%description
Cairo has been designed to let you draw anything you want in a modern
2D graphical user interface.  At the same time, the cairo API has been
designed to be as fun and easy to learn as possible. If you're not
having fun while programming with cairo, then we have failed
somewhere---let us know and we'll try to fix it next time around.

%package devel
Summary: Libraries and headers for developing with libcairo
Group: Development/Libraries
Requires: %{name} >= %{version}
%description devel
Libraries and headers for developing with libcairo

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib} --disable-silent-rules \
  --enable-xlib=no --enable-xlib-xrender=no --enable-xcb-shm=no \
  --enable-egl=no --enable-glx=no --enable-wgl=no --enable-fc=no \
  --enable-pthread=yes --without-x
make

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/gtk-doc

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/libcairo.so.2.11000.2
/usr/%{_lib}/libcairo.so.2
/usr/%{_lib}/libcairo-script-interpreter.so.2.11000.2
/usr/%{_lib}/libcairo-script-interpreter.so.2
/usr/%{_lib}/cairo/libcairo-trace.so.0.0.0
/usr/%{_lib}/cairo/libcairo-trace.so.0
/usr/bin/cairo-trace

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libcairo.so
/usr/%{_lib}/libcairo.la
/usr/%{_lib}/libcairo.a
/usr/%{_lib}/libcairo-script-interpreter.so
/usr/%{_lib}/libcairo-script-interpreter.la
/usr/%{_lib}/libcairo-script-interpreter.a
/usr/%{_lib}/cairo/libcairo-trace.so
/usr/%{_lib}/cairo/libcairo-trace.la
/usr/%{_lib}/cairo/libcairo-trace.a
/usr/%{_lib}/pkgconfig/cairo.pc
/usr/%{_lib}/pkgconfig/cairo-png.pc
/usr/%{_lib}/pkgconfig/cairo-ft.pc
/usr/%{_lib}/pkgconfig/cairo-ps.pc
/usr/%{_lib}/pkgconfig/cairo-pdf.pc
/usr/%{_lib}/pkgconfig/cairo-svg.pc
/usr/include/cairo

%changelog
* Wed May 11 2011 Archaic <lc@diatribe.org>
- Initial version
