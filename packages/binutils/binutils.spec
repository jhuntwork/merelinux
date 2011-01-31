Summary: GNU Binutils
Name: binutils
Version: 2.21
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/binutils
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = ef93235588eb443e4c4a77f229a8d131bccaecc6
BuildRequires: zlib-devel

%description
Provides an assembler, linker and a collection of other tools
necessary for compiling binaries.

%prep
rm -rf %{name}-build
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
rm -fv etc/standards.info
sed -i.bak '/^INFO/s/standards.info //' etc/Makefile.in
mkdir -v ../%{name}-build
cd ../%{name}-build
../%{name}-%{version}/configure \
  --prefix=/usr \
  --enable-shared \
  --libdir=/usr/%{_lib}
make tooldir=/usr

%install
cd ../%{name}-build
make tooldir=/usr DESTDIR=%{buildroot} install
cp ../%{name}-%{version}/include/libiberty.h %{buildroot}/usr/include
rm -f %{buildroot}/usr/share/info/dir
%find_lang bfd
%find_lang binutils
%find_lang gas
%find_lang gprof
%find_lang ld
%find_lang opcodes
cat bfd.lang binutils.lang gas.lang gprof.lang ld.lang opcodes.lang > ../%{name}-%{version}/%{name}.lang
%{compress_man}

%post
for i in as bfd binutils configure gprof ld
do
  /usr/bin/install-info /usr/share/info/$i.info /usr/share/info/dir
done

%preun
for i in as bfd binutils configure gprof ld
do
  /usr/bin/install-info --delete /usr/share/info/$i.info /usr/share/info/dir
done

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/addr2line
/usr/bin/ar
/usr/bin/as
/usr/bin/c++filt
/usr/bin/elfedit
/usr/bin/gprof
/usr/bin/ld
/usr/bin/ld.bfd
/usr/bin/nm
/usr/bin/objcopy
/usr/bin/objdump
/usr/bin/ranlib
/usr/bin/readelf
/usr/bin/size
/usr/bin/strings
/usr/bin/strip
/usr/include/ansidecl.h
/usr/include/bfd.h
/usr/include/bfdlink.h
/usr/include/dis-asm.h
/usr/include/libiberty.h
/usr/include/symcat.h
/usr/lib/ldscripts
/usr/%{_lib}/libbfd-%{version}*
/usr/%{_lib}/libbfd.a
/usr/%{_lib}/libbfd.la
/usr/%{_lib}/libbfd.so
/usr/%{_lib}/libiberty.a
/usr/%{_lib}/libopcodes-%{version}*
/usr/%{_lib}/libopcodes.a
/usr/%{_lib}/libopcodes.la
/usr/%{_lib}/libopcodes.so
/usr/share/info/as.info
/usr/share/info/bfd.info
/usr/share/info/binutils.info
/usr/share/info/configure.info
/usr/share/info/gprof.info
/usr/share/info/ld.info
/usr/share/man/man1/*

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.21-1
- Upgrade to 2.21

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-2
- Fixes to infodir locations

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-1
- Upgrade to 2.20.1

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.20

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
