Summary: GNU C Library 32-bit version
Name: glibc32
Version: 2.10.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube Linux
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/libc
Source: http://ftp.gnu.org/gnu/glibc/glibc-%{version}.tar.bz2

Requires: base-files

%ifarch x86_64
%define my_32 i686-pc-linux-gnu
%endif

%description
The system C library which defines run-time functions for all
C-based software installed in the system. This version is the 32-bit
version for multilib architectures.

%package devel
Summary: Headers, object files and utilities for development using C libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: linux-headers >= %{kernel_version}

%description devel
The %{name}-devel package contains the object files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs).  If you are developing programs which will use
the standard C libraries, your system needs to have these standard
object files available in order to create the executables.

%prep
rm -rf glibc-build
%setup -q -n glibc-%{version}

%build
sed -i '/vi_VN.TCVN/d' localedata/SUPPORTED
sed -i 's|@BASH@|/bin/bash|' elf/ldd.bash.in
mkdir ../glibc-build
cd ../glibc-build
%ifarch x86_64
echo "CFLAGS += -march=i486 -mtune=generic" > configparms
%endif
echo "cross-compiling=no" >> configparms
CC="gcc -m32" CXX="g++ -m32" ../glibc-%{version}/configure --prefix=/usr \
  --host=%{my_32} --build=$(../glibc-%{version}/scripts/config.guess) \
  --disable-profile --enable-add-ons \
  --enable-kernel=2.6.18 --libexecdir=/usr/lib/glibc
make

%install
install -dv %{buildroot}/etc
touch %{buildroot}/etc/ld.so.conf
cd ../glibc-build
make install_root=%{buildroot} install
rm -rf %{buildroot}/usr/{bin,include,sbin,share}
rm -rf %{buildroot}/{etc,sbin}

%clean
rm -rf %{buildroot}
rm -rf glibc-build

%files
%defattr(-,root,root)
/lib/*
/usr/lib/glibc
/usr/lib/gconv

%files devel
%defattr(-,root,root)
/usr/lib/*.o
/usr/lib/*.a
/usr/lib/*.so

%changelog
* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
