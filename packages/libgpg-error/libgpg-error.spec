Summary: libgpg-error
Name: libgpg-error
Version: 1.9
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnupg.org
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 6836579e42320b057a2372bbcd0325130fe2561e 

%description
Libgpg-error is a small library with error codes and descriptions shared by
most GnuPG related software.

%package devel
Summary: Headers and libraries for developing with libgpg-error
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with libgpg-error

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
# Don't need these...
rm -rf %{buildroot}/usr/share/common-lisp
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/gpg-error
/usr/%{_lib}/libgpg-error.so.*

%files devel
%defattr(-,root,root)
/usr/bin/gpg-error-config
/usr/include/gpg-error.h
/usr/%{_lib}/libgpg-error.la
/usr/%{_lib}/libgpg-error.so
/usr/share/aclocal/gpg-error.m4

%changelog
* Thu Sep 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.9-1
- Initial version
