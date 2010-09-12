Summary: PCI Utilities
Name: pciutils
Version: 3.1.7
Release: 1
Group: System Environment/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://mj.ucw.cz/pciutils.html
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 58336ef8c1bbe870f2cc0ed9481a8cf8a58e039c
BuildRequires: zlib-devel

%description
The PCI Utilities are a collection of programs for inspecting and manipulating
configuration of PCI devices, all based on a common portable library libpci
which offers access to the PCI configuration space on a variety of operating
systems.

%package devel
Summary: Headers for developing with pciutils
Group: Development/Libraries
Requires: %{name}

%description devel
Headers for developing with pcituils

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
make PREFIX=/usr LIBDIR=/usr/%{_lib} ZLIB=yes DNS=yes SHARED=yes

%install
make PREFIX=/usr DESTDIR=%{buildroot} install
make PREFIX=/usr LIBDIR=/usr/%{_lib} DESTDIR=%{buildroot} install-lib
ln -sv libpci.so.3.1.7 %{buildroot}/usr/%{_lib}/libpci.so
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
%{buildroot}/usr/sbin/update-pciids
cp -a /usr/share/pci.ids.gz %{buildroot}/usr/share/

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libpci.so.3.1.7
/usr/sbin/lspci
/usr/sbin/setpci
/usr/sbin/update-pciids
/usr/share/man/man7/pcilib.7.bz2
/usr/share/man/man8/lspci.8.bz2
/usr/share/man/man8/setpci.8.bz2
/usr/share/man/man8/update-pciids.8.bz2
/usr/share/pci.ids.gz

%files devel
/usr/include/pci
/usr/%{_lib}/libpci.so
/usr/%{_lib}/pkgconfig/libpci.pc

%changelog
* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.7-1
- Initial version
