Summary: zlib Compression Library
Name: zlib
Version: 1.2.5
Release: 2
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.zlib.net
Source0: http://zlib.net/zlib-1.2.5.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 543fa9abff0442edca308772d6cef85557677e02

%description
According to its maintainers, zlib is:
A Massively Spiffy Yet Delicately Unobtrusive Compression Library

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/%{_lib}
mv -v %{buildroot}/usr/%{_lib}/libz.so.* %{buildroot}/%{_lib}
ln -sfv ../../%{_lib}/libz.so.%{version} %{buildroot}/usr/%{_lib}/libz.so
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/%{_lib}/libz.so.*

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libz.a
/usr/%{_lib}/libz.so
/usr/%{_lib}/pkgconfig/zlib.pc
/usr/share/man/man3/zlib.3.bz2
/usr/include/zconf.h
/usr/include/zlib.h

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 1.2.5-2
- Optimize for size

* Sat Jul 17 2010 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 1.2.5-1
- Upgrade to 1.2.5

* Fri Apr 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.2.4-3
- Fixes to build method since 1.2.4 has a new make system

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.2.4-2
- Move development libraries to the devel package 

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.2.4-1
- Update to 1.2.4

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
