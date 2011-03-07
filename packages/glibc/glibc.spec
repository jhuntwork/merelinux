Summary: GNU C Library
Name: glibc
Version: 2.12.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/libc
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 3ef6d36eee2dc7c4351f215f689e6a04c161a35e

%description
The system C library which defines run-time functions for all
C-based software installed in the system.

%package devel
Summary: Headers, object files and utilities for development using C libraries
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
The %{name}-devel package contains the object files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs).  If you are developing programs which will use
the standard C libraries, your system needs to have these standard
object files available in order to create the executables.

%prep
rm -rf glibc-build
%setup -q
%patch0 -p1
%patch1 -p1
%ifarch x86_64
cd ..
rm -rf glibc-build-32
rm -rf %{name}-%{version}-32
mv -v %{name}-%{version}{,-32}
%setup -q
%patch0 -p1
%patch1 -p1
%endif

%build
%ifarch x86_64
cd ../glibc-%{version}-32
sed -i '/vi_VN.TCVN/d' localedata/SUPPORTED
sed -i 's|@BASH@|/bin/bash|' elf/ldd.bash.in
mkdir ../glibc-build-32
cd ../glibc-build-32
echo "CFLAGS += -march=i486 -mtune=i686" > configparms
echo "cross-compiling=no" >> configparms
CC="gcc -m32" CXX="g++ -m32" \
../glibc-%{version}-32/configure \
  --prefix=/usr \
  --host=i686-pc-linux-gnu \
  --build=x86_64-unknown-linux-gnu \
  --disable-profile \
  --enable-add-ons \
  --enable-kernel=2.6.18 \
  --libexecdir=/usr/lib/glibc \
  --libdir=/usr/lib \
  libc_cv_forced_unwind=yes \
  libc_cv_c_cleanup=yes
make
cd ../glibc-%{version}
%endif
sed -i '/vi_VN.TCVN/d' localedata/SUPPORTED
sed -i 's|@BASH@|/bin/bash|' elf/ldd.bash.in
mkdir ../glibc-build
cd ../glibc-build
%ifarch i686
echo "CFLAGS += -march=i486 -mtune=i686" > configparms
%endif
%if "%{_lib}" != "lib"
echo "slibdir=/lib64" > configparms
%endif
../glibc-%{version}/configure \
  --prefix=/usr \
  --disable-profile \
  --enable-add-ons \
  --enable-kernel=2.6.18 \
  --libexecdir=/usr/%{_lib}/glibc \
  --libdir=/usr/%{_lib}
make

%install
install -dv %{buildroot}/etc
touch %{buildroot}/etc/ld.so.conf
%ifarch x86_64
cd ../glibc-build-32
make install_root=%{buildroot} install
%endif
cd ../glibc-build
make install_root=%{buildroot} install
make install_root=%{buildroot} localedata/install-locales
rm -f %{buildroot}/usr/share/info/dir
rm -f %{buildroot}/etc/localtime
cat > %{buildroot}/etc/nsswitch.conf << "EOF"
# Begin /etc/nsswitch.conf

passwd: files
group: files
shadow: files

hosts: files dns
networks: files

protocols: files
services: files
ethers: files
rpc: files

# End /etc/nsswitch.conf
EOF
cat > %{buildroot}/etc/ld.so.conf << "EOF"
# Begin /etc/ld.so.conf

/usr/local/lib
/opt/lib

# End /etc/ld.so.conf
EOF
%find_lang libc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info /usr/share/info/libc.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/libc.info /usr/share/info/dir

%clean
rm -rf %{buildroot}
rm -rf glibc-build

%files -f ../glibc-build/libc.lang
%defattr(-,root,root)
/etc/ld.so.cache
%config /etc/ld.so.conf
%config /etc/nsswitch.conf
%config /etc/rpc
/%{_lib}/*
/sbin/*
/usr/bin/catchsegv
/usr/bin/gencat
/usr/bin/getconf
/usr/bin/getent
/usr/bin/iconv
/usr/bin/ldd
/usr/bin/lddlibc4
/usr/bin/locale
/usr/bin/localedef
/usr/bin/mtrace
/usr/bin/pcprofiledump
/usr/bin/rpcgen
/usr/bin/sprof
/usr/bin/tzselect
/usr/bin/xtrace
/usr/%{_lib}/glibc
/usr/%{_lib}/gconv
/usr/%{_lib}/locale
/usr/share/locale/locale.alias
/usr/sbin/*
/usr/share/zoneinfo/*
/usr/share/i18n
%ifarch x86_64
/lib/*
/usr/lib/gconv
/usr/lib/glibc
%endif

%files devel
%defattr(-,root,root)
/usr/include/*
/usr/%{_lib}/*.o
/usr/%{_lib}/*.a
/usr/%{_lib}/*.so
/usr/share/info/libc*
%ifarch x86_64
/usr/lib/*.o
/usr/lib/*.a
/usr/lib/*.so
%endif

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.12.2-1
- Upgrade to 2.12.2

* Fri Dec 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.12.1-4
- Upstream security fixes

* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.12.1-3
- Add 32-bit libs for x86_64

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.12.1-2
- Remove /etc/localtime from package - will be created at install-time

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.12.1-1
- Upgrade to 2.12.1

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11.2-1
- Upgrade to 2.11.2

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11.1-2
- Fixes to infodir locations

* Mon Mar 29 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to version 2.11.1

* Fri Dec 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to version 2.11, first build on PowerPC

* Fri Oct 23 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to build with binutils 2.20 and gcc 4.4.2

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
