Summary: GNU dbm
Name: gdbm
Version: 1.8.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gdbm
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 1d1b1d5c0245b1c00aff92da751e9aa1

%package devel
Summary: Libraries and headers for developing with %{name}
Requires: %{name}

%description
GNU dbm is a set of database routines that use extensible hashing.
It works similar to the standard UNIX dbm routines.

%description devel
Libraries and headers for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man
make

%install
make INSTALL_ROOT=%{buildroot} install
make INSTALL_ROOT=%{buildroot} install-compat
rm -f %{buildroot}/usr/info/dir
find %{buildroot} -name "*.la" -exec rm -v '{}' \;

%clean
rm -rf %{buildroot}

%post devel
/usr/bin/install-info /usr/share/info/gdbm.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/gdbm.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/%{_lib}/libgdbm.so.3
/usr/%{_lib}/libgdbm.so.3.0.0
/usr/%{_lib}/libgdbm_compat.so.3
/usr/%{_lib}/libgdbm_compat.so.3.0.0

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libgdbm.a
/usr/%{_lib}/libgdbm.so
/usr/%{_lib}/libgdbm_compat.a
/usr/%{_lib}/libgdbm_compat.so
/usr/include/dbm.h
/usr/include/gdbm.h
/usr/include/ndbm.h
/usr/share/man/man3/gdbm.3
/usr/share/info/gdbm.info

%changelog
* Fri Aug 14 2009 Jeremy Huntwork (jhuntwork at lightcube dot us
- Initial version
