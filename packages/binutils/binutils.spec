Summary: GNU Binutils
Name: binutils
Version: 2.22
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/binutils
Source0: http://ftp.gnu.org/gnu/binutils/binutils-2.22.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 65b304a0b9a53a686ce50a01173d1f40f8efe404
BuildRequires: zlib-devel

%description
Provides an assembler, linker and a collection of other tools
necessary for compiling binaries.

%prep
rm -rf %{name}-build
%setup -q
%{config_musl}

%build
export CFLAGS="-Os -D_GNU_SOURCE"
rm -f etc/standards.info
sed -i '/^INFO/s/standards.info //' etc/Makefile.in
mkdir ../%{name}-build
cd ../%{name}-build
../%{name}-%{version}/configure \
  --prefix='' \
  --disable-shared \
  --disable-werror \
  --disable-nls
make %{PMFLAGS}

%install
cd ../%{name}-build
make DESTDIR=%{buildroot} install
if [ -f %{buildroot}/lib64/libiberty.a ] ; then
  mv %{buildroot}/lib64/libiberty.a %{buildroot}/lib/
  rmdir %{buildroot}/lib64
fi
if [ -d %{buildroot}/x86_64-unknown-linux-musl ] ; then
  mv %{buildroot}/x86_64-unknown-linux-musl/lib/ldscripts %{buildroot}/lib/
  rm -rf %{buildroot}/x86_64-unknown-linux-musl
fi
cp ../%{name}-%{version}/include/libiberty.h %{buildroot}/include
rm -rf %{buildroot}/share/info
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/addr2line
/bin/ar
/bin/as
/bin/c++filt
/bin/elfedit
/bin/gprof
/bin/ld
/bin/ld.bfd
/bin/nm
/bin/objcopy
/bin/objdump
/bin/ranlib
/bin/readelf
/bin/size
/bin/strings
/bin/strip
/include/ansidecl.h
/include/bfd.h
/include/bfdlink.h
/include/dis-asm.h
/include/libiberty.h
/include/symcat.h
/lib/ldscripts
/lib/libbfd.a
/lib/libbfd.la
/lib/libiberty.a
/lib/libopcodes.a
/lib/libopcodes.la
/share/man/man1/*.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.22-1
- Initial version
