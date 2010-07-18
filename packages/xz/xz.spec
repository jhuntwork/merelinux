Summary: XZ Utils
Name: xz
Version: 4.999.9beta
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tukaani.org/xz
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-143-g3e49.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 9e5a42d2b5277d8d71405d065120bd4e

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils are the successor to LZMA Utils.

%package devel
Summary: Libraries and headers for developing with lzma
Group: Development/Libraries
Requires: xz

%description devel
Libraries and headers for developing with lzma

%prep
%setup -q -n %{name}-%{version}-143-g3e49

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make
make check

%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/lzcat
/usr/bin/lzcmp
/usr/bin/lzdiff
/usr/bin/lzegrep
/usr/bin/lzfgrep
/usr/bin/lzgrep
/usr/bin/lzless
/usr/bin/lzma
/usr/bin/lzmadec
/usr/bin/lzmainfo
/usr/bin/lzmore
/usr/bin/unlzma
/usr/bin/unxz
/usr/bin/xz
/usr/bin/xzcat
/usr/bin/xzcmp
/usr/bin/xzdec
/usr/bin/xzdiff
/usr/bin/xzegrep
/usr/bin/xzfgrep
/usr/bin/xzgrep
/usr/bin/xzless
/usr/bin/xzmore
/usr/%{_lib}/liblzma.so.0
/usr/%{_lib}/liblzma.so.0.0.0
/usr/share/doc/xz
/usr/share/man/man1/*

%files devel
%defattr(-,root,root)
/usr/%{_lib}/liblzma.a
/usr/%{_lib}/liblzma.la
/usr/%{_lib}/liblzma.so
/usr/%{_lib}/pkgconfig/liblzma.pc
/usr/include/lzma.h
/usr/include/lzma

%changelog
* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.999.9beta-2
- Upgrade to development snapshot which contains important bug fixes

* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.999.9beta-1
- Initial version
