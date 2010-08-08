Summary: elfutils
Name: elfutils
Version: 0.148
Release: 1
Group: Development/Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://fedorahosted.org/elfutils
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, zlib, bzip2, xz
BuildRequires: digest(%{SOURCE0}) = a0bed1130135f17ad27533b0034dba8d
BuildRequires: zlib-devel, bzip2-devel, xz-devel

%description
Provides utilites for processing ELF files in an
architecture-independent way.

%package libelf
Summary: libelf core library
Group: System Environment/Base

%description libelf
The core libelf library.

%package devel
Summary: Libraries and headers for developing with libelf
Group: Development/Libraries
Requires: elfutils-libelf

%description devel
Libraries and headers for developing with libelf

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
for file in %{buildroot}/usr/bin/*
  do nm=$(basename $file)
  mv -v $file %{buildroot}/usr/bin/eu-$nm
done
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/eu-addr2line
/usr/bin/eu-ar
/usr/bin/eu-elfcmp
/usr/bin/eu-elflint
/usr/bin/eu-findtextrel
/usr/bin/eu-ld
/usr/bin/eu-make-debug-archive
/usr/bin/eu-nm
/usr/bin/eu-objdump
/usr/bin/eu-ranlib
/usr/bin/eu-readelf
/usr/bin/eu-size
/usr/bin/eu-strings
/usr/bin/eu-strip
/usr/bin/eu-unstrip

%files libelf
%defattr(-,root,root)
%dir /usr/%{_lib}/elfutils/
/usr/%{_lib}/elfutils/libebl_alpha-0.148.so
/usr/%{_lib}/elfutils/libebl_arm-0.148.so
/usr/%{_lib}/elfutils/libebl_i386-0.148.so
/usr/%{_lib}/elfutils/libebl_ia64-0.148.so
/usr/%{_lib}/elfutils/libebl_ppc-0.148.so
/usr/%{_lib}/elfutils/libebl_ppc64-0.148.so
/usr/%{_lib}/elfutils/libebl_s390-0.148.so
/usr/%{_lib}/elfutils/libebl_sh-0.148.so
/usr/%{_lib}/elfutils/libebl_sparc-0.148.so
/usr/%{_lib}/elfutils/libebl_x86_64-0.148.so
/usr/%{_lib}/libasm-0.148.so
/usr/%{_lib}/libasm.so.1
/usr/%{_lib}/libdw-0.148.so
/usr/%{_lib}/libdw.so.1
/usr/%{_lib}/libelf-0.148.so
/usr/%{_lib}/libelf.so.1

%files devel
%defattr(-,root,root)
/usr/include/dwarf.h
/usr/include/elfutils
/usr/include/gelf.h
/usr/include/libelf.h
/usr/include/nlist.h
/usr/%{_lib}/elfutils/libebl_alpha.so
/usr/%{_lib}/elfutils/libebl_arm.so
/usr/%{_lib}/elfutils/libebl_i386.so
/usr/%{_lib}/elfutils/libebl_ia64.so
/usr/%{_lib}/elfutils/libebl_ppc.so
/usr/%{_lib}/elfutils/libebl_ppc64.so
/usr/%{_lib}/elfutils/libebl_s390.so
/usr/%{_lib}/elfutils/libebl_sh.so
/usr/%{_lib}/elfutils/libebl_sparc.so
/usr/%{_lib}/elfutils/libebl_x86_64.so
/usr/%{_lib}/libasm.a
/usr/%{_lib}/libasm.so
/usr/%{_lib}/libdw.a
/usr/%{_lib}/libdw.so
/usr/%{_lib}/libebl.a
/usr/%{_lib}/libelf.a
/usr/%{_lib}/libelf.so

%changelog
* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.148-1
- Initial version
