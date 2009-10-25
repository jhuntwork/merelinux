Summary: GNU C Library
Name: glibc
Version: 2.10.1
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/libc
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-binutils-1.patch

Requires: base-files
BuildRequires: digest(%{SOURCE0}) = ee71dedf724dc775e4efec9b823ed3be

%description
The system C library which defines run-time functions for all
C-based software installed in the system.

%package devel
Summary: Headers, object files and utilities for development using C libraries
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}, texinfo
Requires: linux-headers

%description devel
The %{name}-devel package contains the object files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs).  If you are developing programs which will use
the standard C libraries, your system needs to have these standard
object files available in order to create the executables.

%prep
rm -rf glibc-build
%setup -q -n glibc-%{version}
%patch -p1 %{PATCH0}

%build
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
../glibc-%{version}/configure --prefix=/usr \
  --disable-profile --enable-add-ons \
  --enable-kernel=2.6.18 --libexecdir=/usr/%{_lib}/glibc \
  --libdir=/usr/%{_lib}
make

%install
install -dv %{buildroot}/etc
touch %{buildroot}/etc/ld.so.conf
cd ../glibc-build
make install_root=%{buildroot} install
make install_root=%{buildroot} localedata/install-locales
rm -f %{buildroot}%{_infodir}/dir
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
rm -f %{buildroot}/usr/share/info/dir
%find_lang libc

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info %{_infodir}/libc.info %{_infodir}/dir

%preun devel
/usr/bin/install-info --delete %{_infodir}/libc.info %{_infodir}/dir

%clean
rm -rf %{buildroot}
rm -rf glibc-build

%files -f ../glibc-build/libc.lang
%defattr(-,root,root)
/etc/ld.so.cache
/etc/ld.so.conf
/etc/localtime
/etc/nsswitch.conf
/etc/rpc
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

%files devel
%defattr(-,root,root)
/usr/include/*
/usr/%{_lib}/*.o
/usr/%{_lib}/*.a
/usr/%{_lib}/*.so
/usr/share/info/libc*

%changelog
* Fri Oct 23 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Updated to build with binutils 2.20 and gcc 4.4.2
* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
