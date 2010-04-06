Summary: pkg-config 
Name: pkg-config
Version: 0.23
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pkg-config.freedesktop.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = d922a88782b64441d06547632fd85744

Requires: base-layout, glibc
Provides: pkgconfig

%description
pkg-config is a helper tool used when compiling applications and libraries. It can
be used to determine library versions and compiler options needed for linking to
installed libraries.

%prep
%setup -q

%build
./configure --prefix=/usr --with-pc-path=/usr/%{_lib}/pkgconfig
make
make check

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/usr/share/pkgconfig
install -dv %{buildroot}/usr/%{_lib}/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/pkg-config
/usr/share/aclocal/pkg.m4
/usr/share/pkgconfig
/usr/%{_lib}/pkgconfig
/usr/share/man/man1/pkg-config.1

%changelog
* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.23-1
- Initial version
