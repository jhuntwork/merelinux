Summary: XZ Utils
Name: xz
Version: 5.0.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://tukaani.org/xz
Source0: http://tukaani.org/xz/xz-5.0.3.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 79661fd1c24603437e325d76732046b1da683b32

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils are the successor to LZMA Utils.

%package devel
Summary: Libraries and headers for developing with lzma
Group: Development/Libraries

%description devel
Libraries and headers for developing with lzma

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
export LDFLAGS="--static"
./configure \
  --prefix='' \
  --disable-shared
make %{PMFLAGS}
#make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/lzcat
/bin/lzcmp
/bin/lzdiff
/bin/lzegrep
/bin/lzfgrep
/bin/lzgrep
/bin/lzless
/bin/lzma
/bin/lzmadec
/bin/lzmainfo
/bin/lzmore
/bin/unlzma
/bin/unxz
/bin/xz
/bin/xzcat
/bin/xzcmp
/bin/xzdec
/bin/xzdiff
/bin/xzegrep
/bin/xzfgrep
/bin/xzgrep
/bin/xzless
/bin/xzmore
/share/man/man1/*.bz2

%files devel
%defattr(-,root,root)
/lib/liblzma.a
/lib/liblzma.la
/lib/pkgconfig/liblzma.pc
/include/lzma.h
/include/lzma

%files extras
/share/doc/xz

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.0.3-1
- Initial version
