Summary: The GNU Compiler Collection
Name: gcc
Version: 4.5.3
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://gcc.gnu.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 73c45dfda5eef6b124be53e56828b5925198cc1b
BuildRequires: gmp-devel
BuildRequires: mpfr-devel
BuildRequires: mpc-devel
BuildRequires: ppl-devel
BuildRequires: cloog-ppl-devel
BuildRequires: zlib-devel
BuildRequires: elfutils-devel
BuildRequires: tcl
BuildRequires: expect
BuildRequires: dejagnu

%description
The GNU Compiler Collection is required to compile various languages.

%package libs
Summary: GCC support libraries
Group: System Environment/Libraries

%description libs
The %{name}-libs package contains support libraries for programs
compiled using GCC.

%package c++
Summary: GCC C++ compiler
Group: Development/Tools
Requires: %{name} = %{version}
Requires: %{name}-c++-libs = %{version}

%description c++
The %{name}-c++ package contains a C++ compiler to be used with GCC.
It includes support for most of the current C++ specification, including
templates and exception handling.

%package c++-libs
Summary: GCC C++ support libraries
Group: System Environment/Libraries
Requires: %{name}-libs = %{version}

%description c++-libs
The %{name}-c++-libs package contains support libraries for programs
compiled using GCC C++.

%prep
rm -rf %{name}-build
%setup -q

%build
sed -i 's/install_to_$(INSTALL_DEST) //' libiberty/Makefile.in
sed -i 's,\./fixinc\.sh,-c true,' gcc/Makefile.in
%ifarch i686
sed -i 's/^T_CFLAGS =$$/& -fomit-frame-pointer/' gcc/Makefile.in
%endif
mkdir -v ../%{name}-build
cd ../%{name}-build
../%{name}-%{version}/configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib} \
  --with-system-zlib \
  --enable-shared \
  --enable-threads=posix \
  --enable-__cxa_atexit \
  --enable-clocale=gnu \
  --enable-languages=c,c++ \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man 
make %{PMFLAGS} LDFLAGS="-s"
make %{PMFLAGS} -k check || /bin/true
../%{name}-%{version}/contrib/test_summary 2>&1 | grep -A7 Summ | tee check.log

%install
cd ../%{name}-build
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/%{_lib}
install -dv %{buildroot}/lib
ln -sv ../usr/bin/cpp %{buildroot}/%{_lib}
ln -sfv ../usr/bin/cpp %{buildroot}/lib
ln -sv gcc %{buildroot}/usr/bin/cc
mv %{buildroot}/usr/%{_lib}/*.py %{buildroot}/usr/share/gcc-%{version}/python/
%if "%{_lib}" != "lib"
rm -f %{buildroot}/usr/lib/*.py
%endif
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}
%find_lang cpplib
%find_lang libstdc++
cat %{name}.lang cpplib.lang > ../%{name}-%{version}/%{name}.lang

%post
for i in cpp cppinternals gcc gccinstall gccint libgomp
do
  /usr/bin/install-info /usr/share/info/$i.info /usr/share/info/dir
done

%preun
for i in cpp cppinternals gcc gccinstall gccint libgomp
do
  /usr/bin/install-info --delete /usr/share/info/$i.info /usr/share/info/dir
done

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%post c++-libs -p /sbin/ldconfig
%postun c++-libs -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%if "%{_lib}" != "lib"
/lib/cpp
%endif
/%{_lib}/cpp
/usr/bin/cc
/usr/bin/cpp
/usr/bin/gcc
/usr/bin/gccbug
/usr/bin/gcov
/usr/bin/*-linux-gnu-gcc
/usr/bin/*-linux-gnu-gcc-%{version}
/usr/share/info/cpp.info
/usr/share/info/cppinternals.info
/usr/share/info/gcc.info
/usr/share/info/gccinstall.info
/usr/share/info/gccint.info
/usr/share/info/libgomp.info
/usr/%{_lib}/gcc
/usr/%{_lib}/libgcc_s.so
/usr/%{_lib}/libgomp.a
/usr/%{_lib}/libgomp.so
/usr/%{_lib}/libgomp.spec
/usr/%{_lib}/libmudflap.a
/usr/%{_lib}/libmudflap.so
/usr/%{_lib}/libmudflapth.a
/usr/%{_lib}/libmudflapth.so
/usr/%{_lib}/libssp.a
/usr/%{_lib}/libssp.so
/usr/%{_lib}/libssp_nonshared.a
/usr/%{_lib}/libgomp.la
/usr/%{_lib}/libmudflap.la
/usr/%{_lib}/libmudflapth.la
/usr/%{_lib}/libssp.la
/usr/%{_lib}/libssp_nonshared.la
/usr/share/man/man1/gcov*
/usr/share/man/man1/gcc*
/usr/share/man/man1/cpp*
/usr/share/man/man7/*
%if "%{_lib}" != "lib"
/usr/lib/libgcc_s.so
/usr/lib/libgomp.a
/usr/lib/libgomp.la
/usr/lib/libgomp.so
/usr/lib/libgomp.spec
/usr/lib/libmudflap.a
/usr/lib/libmudflap.la
/usr/lib/libmudflap.so
/usr/lib/libmudflapth.a
/usr/lib/libmudflapth.la
/usr/lib/libmudflapth.so
/usr/lib/libssp.a
/usr/lib/libssp.la
/usr/lib/libssp.so
/usr/lib/libssp_nonshared.a
/usr/lib/libssp_nonshared.la
%endif

%files libs
%defattr(-,root,root)
/usr/%{_lib}/libgcc_s.so.*
/usr/%{_lib}/libgomp.so.*
/usr/%{_lib}/libmudflap.so.*
/usr/%{_lib}/libmudflapth.so.*
/usr/%{_lib}/libssp.so.*
%if "%{_lib}" != "lib"
/usr/lib/libgcc_s.so.*
/usr/lib/libgomp.so.*
/usr/lib/libmudflap.so.*
/usr/lib/libmudflapth.so.*
/usr/lib/libssp.so.*
%endif

%files c++ -f ../%{name}-build/libstdc++.lang
%defattr(-,root,root)
/usr/bin/c++
/usr/bin/g++
/usr/bin/*-linux-gnu-c++
/usr/bin/*-linux-gnu-g++
/usr/include/c++
/usr/%{_lib}/libstdc++.a
/usr/%{_lib}/libstdc++.so
/usr/%{_lib}/libsupc++.a
/usr/%{_lib}/libstdc++.la
/usr/%{_lib}/libsupc++.la
/usr/share/man/man1/g++*
%if "%{_lib}" != "lib"
/usr/lib/libstdc++.a
/usr/lib/libstdc++.la
/usr/lib/libstdc++.so
/usr/lib/libsupc++.a
/usr/lib/libsupc++.la
%endif

%files c++-libs
%defattr(-,root,root)
/usr/share/gcc-%{version}
/usr/%{_lib}/libstdc++.so.*
%if "%{_lib}" != "lib"
/usr/lib/libstdc++.so.*
%endif

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.5.3-1
- Upgrade to 4.5.3, fix missing /lib/cpp symlink in 64bit arch

* Sun Dec 19 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.5.2-1
- Upgrade to 4.5.2

* Thu Aug 05 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.5.1-1
- Upgrade to 4.5.1 and enable multilib

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.5.0-1
- Upgrade to 4.5.0

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.3-2
- Fixes to infodir locations

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.3-1
- Upgrade to 4.4.3

* Tue Dec 29 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.2-2
- Add in support for PowerPC

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.4.2-1
- Upgrade to 4.4.2

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
