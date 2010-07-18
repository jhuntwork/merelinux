Summary: The Parma Polyhedra Library
Name: ppl
Version: 0.10.2
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.cs.unipr.it/ppl
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-upstream_fixes-1.patch

Requires: base-layout, glibc, gmp
BuildRequires: digest(%{SOURCE0}) = 5667111f53150618b0fa522ffc53fc3e
BuildRequires: digest(%{PATCH0}) = f051ea3dbdc20c5567490978e5faf368
BuildRequires: gmp-devel

%package devel
Summary: Headers and object files for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description
The Parma Polyhedra Library (PPL) provides numerical abstractions
especially targeted at applications in the field of analysis and
verification of complex systems.

%description devel
Provides headers and object files for use in developing
applications using %{name}.

%prep
%setup -q
%patch0 -p1

%build
autoreconf -f
./configure --prefix=/usr --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/ppl_lcdd
/usr/%{_lib}/libppl.so.7
/usr/%{_lib}/libppl.so.7.1.0
/usr/%{_lib}/libppl_c.so.2
/usr/%{_lib}/libppl_c.so.2.1.0
/usr/%{_lib}/libpwl.so.4
/usr/%{_lib}/libpwl.so.4.0.0
/usr/share/man/man1/ppl_lcdd.1

%files devel
%defattr(-,root,root)
/usr/bin/ppl-config
/usr/include/ppl_c.h
/usr/include/ppl.hh
/usr/include/pwl.hh
/usr/share/aclocal/ppl.m4
/usr/share/aclocal/ppl_c.m4
/usr/share/doc/ppl
/usr/share/doc/pwl
/usr/%{_lib}/libppl.a
/usr/%{_lib}/libppl.la
/usr/%{_lib}/libppl.so
/usr/%{_lib}/libppl_c.a
/usr/%{_lib}/libppl_c.la
/usr/%{_lib}/libppl_c.so
/usr/%{_lib}/libpwl.a
/usr/%{_lib}/libpwl.la
/usr/%{_lib}/libpwl.so
/usr/share/man/man1/ppl-config.1
/usr/share/man/man3/libppl.3
/usr/share/man/man3/libppl_c.3

%changelog
* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.10.2-1
- Initial version
