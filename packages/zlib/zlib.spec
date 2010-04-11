Summary: zlib Compression Library
Name: zlib
Version: 1.2.4
Release: 2
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.zlib.net
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 763c6a0b4ad1cdf5549e3ab3f140f4cb

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
./configure --prefix=/usr --libdir=%{buildroot}/usr/%{_lib}
make

%install
make install prefix=%{buildroot}/usr
make clean
./configure --prefix=/usr --shared --libdir=%{buildroot}/usr/%{_lib}
make
make install prefix=%{buildroot}/usr
install -dv %{buildroot}/%{_lib}
mv -v %{buildroot}/usr/%{_lib}/libz.so.* %{buildroot}/%{_lib}
ln -sfv ../../%{_lib}/libz.so.%{version} %{buildroot}/usr/%{_lib}/libz.so
chmod 644 %{buildroot}/usr/%{_lib}/libz.a

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/%{_lib}/libz.so.*

%files devel
%defattr(-,root,root)
%attr(0644,root,root) /usr/%{_lib}/libz.a
/usr/%{_lib}/libz.so
/usr/%{_lib}/pkgconfig/zlib.pc
/usr/share/man/man3/zlib.3
/usr/include/zconf.h
/usr/include/zlib.h

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.2.4-2
- Move development libraries to the devel package 

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.2.4-1
- Update to 1.2.4

* Sun Jul 19 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
