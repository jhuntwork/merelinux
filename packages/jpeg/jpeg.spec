Summary: jpeg
Name: jpeg
Version: 8b
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.ijg.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}src.v%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = e022acbc5b36cd2cb70785f5b575661e

%description
jpeg contains a free library for JPEG compression

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/cjpeg
/usr/bin/djpeg
/usr/bin/jpegtran
/usr/bin/rdjpgcom
/usr/bin/wrjpgcom
/usr/%{_lib}/libjpeg.so.8
/usr/%{_lib}/libjpeg.so.8.0.2
/usr/share/man/man1/cjpeg.1
/usr/share/man/man1/djpeg.1
/usr/share/man/man1/jpegtran.1
/usr/share/man/man1/rdjpgcom.1
/usr/share/man/man1/wrjpgcom.1

%files devel
%defattr(-,root,root)
/usr/include/jconfig.h
/usr/include/jerror.h
/usr/include/jmorecfg.h
/usr/include/jpeglib.h
/usr/%{_lib}/libjpeg.a
/usr/%{_lib}/libjpeg.la
/usr/%{_lib}/libjpeg.so

%changelog
* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8b-1
- Initial version
