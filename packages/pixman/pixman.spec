Summary: The pixel-manipulation library for X and cairo.
Name: pixman
Version: 0.22.0
Release: 1
Group: System Environment/Base
License: MIT
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://cgit.freedesktop.org/pixman/
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = da0a9c63fa315f163a32c7e40dd0b2a0f88c0d21

%description
pixman is a library that provides low-level pixel manipulation
features such as image compositing and trapezoid rasterization.

%package devel
Summary: Libraries and headers for developing with 
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with libpixman

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib} --disable-silent-rules
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/libpixman-1.so.0.22.0
/usr/%{_lib}/libpixman-1.so.0

%files devel
%defattr(-,root,root)
/usr/include/pixman-1
/usr/%{_lib}/libpixman-1.so
/usr/%{_lib}/libpixman-1.la
/usr/%{_lib}/libpixman-1.a
/usr/%{_lib}/pkgconfig/pixman-1.pc

%changelog
* Tue May 10 2011 Archaic <lc@diatribe.org>
- Initial version
