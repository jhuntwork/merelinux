Summary: The CLooG Code Generator in the Polyhedral Model
Name: cloog-ppl
Version: 0.15.9
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://gcc.gnu.org/wiki/CLooG-PPL
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, gmp, ppl
BuildRequires: digest(%{SOURCE0}) = 806e001d1b1a6b130069ff6274900af5 
BuildRequires: ppl-devel, gmp-devel

%description
CLooG is a free software and library to generate code for scanning Z-polyhedra.
Cloog-PPL uses the PPL library instead of PolyLib for polyhedral functions. 

%package devel
Summary: Headers, object files and info pages for developing with %{name}
Group: Development/Libraries
Requires: %{name}
Requires(post): texinfo, bash, ncurses, readline

%description devel
Provides headers, object files and info pages for use in developing
applications using %{name}.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-ppl=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%post devel
/usr/bin/install-info /usr/share/info/cloog.info /usr/share/info/dir

%preun devel
/usr/bin/install-info --delete /usr/share/info/cloog.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/cloog
/usr/%{_lib}/libcloog.so.0
/usr/%{_lib}/libcloog.so.0.0.0

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libcloog.so
/usr/%{_lib}/libcloog.a
/usr/%{_lib}/libcloog.la
/usr/share/info/cloog.info
/usr/include/cloog

%changelog
* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.15.9-1
- Initial version
