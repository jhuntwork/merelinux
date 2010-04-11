Summary: GNU Binutils
Name: binutils
Version: 2.20.1
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/binutils
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, glibc-devel, linux-headers, zlib, texinfo
BuildRequires: digest(%{SOURCE0}) = 9cdfb9d6ec0578c166d3beae5e15c4e5

%description
Provides an assembler, linker and a collection of other tools
necessary for compiling binaries.

%prep
rm -rf %{name}-build
%setup -q

%build
rm -fv etc/standards.info
sed -i.bak '/^INFO/s/standards.info //' etc/Makefile.in
mkdir -v ../%{name}-build
cd ../%{name}-build
../%{name}-%{version}/configure --prefix=/usr --enable-shared \
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

%post
for i in as bfd binutils configure gprof ld
do
  /usr/bin/install-info %{_infodir}/$i.info %{_infodir}/dir
done

%preun
for i in as bfd binutils configure gprof ld
do
  /usr/bin/install-info --delete %{_infodir}/$i.info %{_infodir}/dir
done

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/addr2line
/usr/bin/ar
/usr/bin/as
/usr/bin/c++filt
/usr/bin/gprof
/usr/bin/ld
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
/usr/%{_lib}/libbfd-2.20.1.20100303.so
/usr/%{_lib}/libbfd.a
/usr/%{_lib}/libbfd.la
/usr/%{_lib}/libbfd.so
/usr/%{_lib}/libiberty.a
/usr/%{_lib}/libopcodes-2.20.1.20100303.so
/usr/%{_lib}/libopcodes.a
/usr/%{_lib}/libopcodes.la
/usr/%{_lib}/libopcodes.so
/usr/share/info/as.info
/usr/share/info/bfd.info
/usr/share/info/binutils.info
/usr/share/info/configure.info
/usr/share/info/gprof.info
/usr/share/info/ld.info
/usr/share/man/man1/addr2line.1
/usr/share/man/man1/ar.1
/usr/share/man/man1/as.1
/usr/share/man/man1/c++filt.1
/usr/share/man/man1/dlltool.1
/usr/share/man/man1/gprof.1
/usr/share/man/man1/ld.1
/usr/share/man/man1/nlmconv.1
/usr/share/man/man1/nm.1
/usr/share/man/man1/objcopy.1
/usr/share/man/man1/objdump.1
/usr/share/man/man1/ranlib.1
/usr/share/man/man1/readelf.1
/usr/share/man/man1/size.1
/usr/share/man/man1/strings.1
/usr/share/man/man1/strip.1
/usr/share/man/man1/windmc.1
/usr/share/man/man1/windres.1


%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-1
- Upgrade to 2.20.1

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.20

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
