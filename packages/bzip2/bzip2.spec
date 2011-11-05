Summary: bzip2 
Name: bzip2
Version: 1.0.6
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.bzip2.org
Source0: http://bzip.org/1.0.6/bzip2-1.0.6.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 3f89f861209ce81a6bab1fd1998c0ef311712002

%package devel
Summary: Libraries and headers for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description
bzip2 is high-quality data compressor.

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q
sed -i 's@-O2@-Os -pipe@' Makefile
sed -i 's@-O2@-Os -pipe@' Makefile-libbz2_so

%build
sed -i 's@\(ln -s -f \)$(PREFIX)/bin/@\1@' Makefile
sed -i "s@(PREFIX)/man@(PREFIX)/share/man@g" Makefile
make %{PMFLAGS} -f Makefile-libbz2_so
make clean
make %{PMFLAGS}

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
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/bunzip2
/bin/bzcat
/bin/bzip2
/%{_lib}/libbz2.so.*
/usr/bin/bzcmp
/usr/bin/bzdiff
/usr/bin/bzegrep
/usr/bin/bzfgrep
/usr/bin/bzgrep
/usr/bin/bzip2recover
/usr/bin/bzless
/usr/bin/bzmore
/usr/share/man/man1/*.bz2

%files devel
/usr/%{_lib}/libbz2.a
/usr/%{_lib}/libbz2.so
/usr/include/bzlib.h

%changelog
* Sat Nov 05 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.6-2
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.6-1
- Upgrade to 1.0.6

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.5-2
- Fix lib version to match binary version

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.5-1
- Initial version
