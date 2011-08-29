Summary: XZ Utils
Name: xz
Version: 5.0.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tukaani.org/xz
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = c244dfffef4196b997035d7389e957f56a3a87d1

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils are the successor to LZMA Utils.

%package devel
Summary: Libraries and headers for developing with lzma
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with lzma

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

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
/usr/%{_lib}/liblzma.so.*
/usr/share/doc/xz
/usr/share/man/man1/*.bz2

%files devel
%defattr(-,root,root)
/usr/%{_lib}/liblzma.a
/usr/%{_lib}/liblzma.la
/usr/%{_lib}/liblzma.so
/usr/%{_lib}/pkgconfig/liblzma.pc
/usr/include/lzma.h
/usr/include/lzma

%changelog
* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.0.2-1
- Upgrade to 5.0.2

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.0.1-1
- Upgrade to 5.0.1

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.999.9beta-2
- Upgrade to development snapshot which contains important bug fixes

* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.999.9beta-1
- Initial version
