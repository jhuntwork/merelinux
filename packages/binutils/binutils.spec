Summary: GNU Binutils
Name: binutils
Version: 2.20
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/binutils
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-genscripts_multilib-1.patch

Requires: base-layout, glibc, glibc-devel, linux-headers, zlib, texinfo

%description
Provides an assembler, linker and a collection of other tools
necessary for compiling binaries.

%prep
rm -rf %{name}-build
%setup -q

%build
%if %{_lib} != "lib"
patch -Np1 -i %{SOURCE1}
%endif
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

%files
%defattr(-,root,root)
/usr/lib/*
%if %{_lib} != "lib"
/usr/%{_lib}/*
%endif
/usr/bin/*
/usr/include/*
/usr/share/man/man1/*
/usr/share/locale/*
/usr/share/info/*

%changelog
* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.20

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
