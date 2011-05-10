Summary: A free, high quality, and portable, font engine
Name: freetype
Version: 2.4.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://freetype.sourceforge.net/index2.html
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 1d136cbc51c67b212c91ba04dc5db797f35e64e6

%description
FreeType 2 is a software font engine that is designed to be small, efficient,
highly customizable, and portable while capable of producing high-quality output
(glyph images). It can be used in graphics libraries, display servers, font
conversion tools, text image generation tools, and many other products as well.

%package devel
Summary: Libraries and headers for developing with libfreetype
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with libfreetype

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/%{_lib}/libfreetype.so.6.6.2
/usr/%{_lib}/libfreetype.so.6

%files devel
%defattr(-,root,root)
/usr/bin/freetype-config
/usr/include/freetype2
/usr/include/ft2build.h
/usr/%{_lib}/libfreetype.so
/usr/%{_lib}/libfreetype.la
/usr/%{_lib}/libfreetype.a
/usr/%{_lib}/pkgconfig/freetype2.pc
/usr/share/aclocal/freetype2.m4

%changelog
* Mon May 09 2011 Archaic <lc@8bitnet.com> 
- Initial version
