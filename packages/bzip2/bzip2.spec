Summary: bzip2 
Name: bzip2
Version: 1.0.5
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.bzip2.org/
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-version_fixes-1.patch

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 3c15a0c8d1d3ee1c46a1634d00617b1a
BuildRequires: digest(%{PATCH0}) =  e373fcd16bac28d6e53a268b875bfd8c

%package devel
Summary: Libraries and headers for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description
%{name} is high-quality data compressor.

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q
%patch0 -p1

%build
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
make -f Makefile-libbz2_so
make clean
make

%install
make PREFIX=%{buildroot}/usr install
%if "%{_lib}" == "lib64"
  mkdir %{buildroot}/usr/lib64
  mv %{buildroot}/usr/lib/libbz2.a %{buildroot}/usr/lib64
%endif
mkdir %{buildroot}/{bin,%{_lib}}
cp -v bzip2-shared %{buildroot}/bin/bzip2
cp -av libbz2.so* %{buildroot}/%{_lib}
ln -sv ../../%{_lib}/libbz2.so.1.0 %{buildroot}/usr/%{_lib}/libbz2.so
rm -v %{buildroot}/usr/bin/{bunzip2,bzcat,bzip2}
ln -sv bzip2 %{buildroot}/bin/bunzip2
ln -sv bzip2 %{buildroot}/bin/bzcat

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/bunzip2
/bin/bzcat
/bin/bzip2
/%{_lib}/libbz2.so.1.0
/%{_lib}/libbz2.so.1.0.5
/usr/bin/bzcmp
/usr/bin/bzdiff
/usr/bin/bzegrep
/usr/bin/bzfgrep
/usr/bin/bzgrep
/usr/bin/bzip2recover
/usr/bin/bzless
/usr/bin/bzmore
/usr/share/man/man1/bzcmp.1
/usr/share/man/man1/bzdiff.1
/usr/share/man/man1/bzegrep.1
/usr/share/man/man1/bzfgrep.1
/usr/share/man/man1/bzgrep.1
/usr/share/man/man1/bzip2.1
/usr/share/man/man1/bzless.1
/usr/share/man/man1/bzmore.1

%files devel
/usr/%{_lib}/libbz2.a
/usr/%{_lib}/libbz2.so
/usr/include/bzlib.h

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.5-2
- Fix lib version to match binary version

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.5-1
- Initial version
