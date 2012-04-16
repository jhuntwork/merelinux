Summary: The GNU Compiler Collection
Name: gcc
Version: 4.2.4
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://gcc.gnu.org
Source0: http://ftp.gnu.org/gnu/gcc/gcc-%{version}/%{name}-%{version}.tar.bz2

Requires: binutils
Requires: musl-devel
BuildRequires: digest(sha1:%{SOURCE0}) = bb20efc7750fe0d6172c5945572bf036fe59d3dd
BuildRequires: zlib-devel
#BuildRequires: tcl
#BuildRequires: expect
#BuildRequires: dejagnu

%description
The GNU Compiler Collection is required to compile various languages.

%package c++
Summary: GCC C++ compiler
Group: Development/Tools
Requires: %{name} = %{version}

%description c++
The gcc-c++ package contains a C++ compiler to be used with GCC.
It includes support for most of the current C++ specification, including
templates and exception handling.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
locale messages and extra documentation

%prep
rm -rf %{name}-build
%setup -q
%{config_musl}
sed -i 's/install_to_$(INSTALL_DEST) //' libiberty/Makefile.in
sed -i 's,\./fixinc\.sh,-c true,' gcc/Makefile.in
for file in $(find gcc/config/i386 -name linux64.h -o -name linux.h)
do
	sed -i \
	-e 's@/usr@/@g' \
	-e 's@lib/ld-linux.so.2@lib/ld-musl-i386.so.1@' \
        -e 's@lib64/ld-linux-x86-64.so.2@lib/ld-musl-x86_64.so.1@' $file
done
# Just use /lib - no lib64 since we're not doing multilib
sed -i '/MULTILIB_OSDIRNAMES/d' `find gcc/config -name t-linux64`
# Remove glibc specfic header include
sed -i '/include <link.h>/s@^.*@/\*&\*/@' gcc/unwind-dw2-fde-glibc.c
# Fix include directory locations
sed -i '/^NATIVE_SYSTEM_HEADER_DIR/s@= .*@= /include@' gcc/Makefile.in
sed -i '/#define STANDARD_INCLUDE_DIR/s@"/usr/include"@"/include"@g' gcc/cppdefault.c
# Trade out c++ specific config for generic
rm -rf libstdc++-v3/config/os/gnu-linux
ln -s generic ./libstdc++-v3/config/os/gnu-linux

%build
mkdir ../%{name}-build
cd ../%{name}-build
export CFLAGS='-Os -D_GNU_SOURCE'
../%{name}-%{version}/configure \
  --prefix='' \
  --libdir=/lib \
  --libexecdir=/lib \
  --with-system-zlib \
  --disable-multilib \
  --disable-bootstrap \
  --disable-libssp \
  --disable-libmudflap \
  --disable-libgomp \
  --disable-shared \
  --enable-languages=c,c++ \
  --infodir=/share/info \
  --mandir=/share/man 
make %{PMFLAGS} BOOT_LDFLAGS="-static" LDFLAGS="-static"
#make %{PMFLAGS} -k check || /bin/true
#../%{name}-%{version}/contrib/test_summary 2>&1 | grep -A7 Summ | tee check.log

%install
cd ../%{name}-build
make DESTDIR=%{buildroot} install
install -d %{buildroot}/lib
install -d %{buildroot}/lib
ln -s ../bin/cpp %{buildroot}/lib
ln -sf ../bin/cpp %{buildroot}/lib
ln -s gcc %{buildroot}/bin/cc
rm -rf %{buildroot}/share/info
# Don't need the arch specific hard links
rm %{buildroot}/bin/%{_arch}-*
%{compress_man}
%{strip}
%find_lang %{name}
%find_lang cpplib
cat %{name}.lang cpplib.lang > ../%{name}-%{version}/%{name}.lang
if [ -d %{buildroot}/lib64 ] ; then
  mv %{buildroot}/lib64/* %{buildroot}/lib/
  rmdir %{buildroot}/lib64
fi

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/lib/cpp
/bin/cc
/bin/cpp
/bin/gcc
/bin/gccbug
/bin/gcov
/lib/gcc
/share/man/man1/cpp*.bz2
/share/man/man1/gcov*.bz2
/share/man/man1/gcc*.bz2
/share/man/man7/*.bz2

%files c++
%defattr(-,root,root)
/bin/c++
/bin/g++
/include/c++
/lib/libstdc++.a
/lib/libstdc++.la
/lib/libsupc++.a
/lib/libsupc++.la
/share/man/man1/g++.1.bz2

%files extras -f %{name}.lang
%defattr(-,root,root)

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.4-1
- Initial version
