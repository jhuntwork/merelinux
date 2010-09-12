Summary: libgcrypt
Name: libgcrypt
Version: 1.4.6
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnupg.org
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 445b9e158aaf91e24eae3d1040c6213e9d9f5ba6
BuildRequires: libgpg-error-devel

%description
Libgcrypt is GNU's basic cryptographic library.

%package devel
Summary: Headers and libraries for developing with libgcrypt
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with libgcrypt

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
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig
/usr/bin/install-info /usr/share/info/gcrypt.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/gcrypt.info /usr/share/info/dir

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/dumpsexp
/usr/bin/hmac256
/usr/share/info/gcrypt.info

/usr/%{_lib}/libgcrypt.so.*

%files devel
%defattr(-,root,root)
/usr/bin/libgcrypt-config
/usr/include/gcrypt-module.h
/usr/include/gcrypt.h
/usr/%{_lib}/libgcrypt.a
/usr/%{_lib}/libgcrypt.la
/usr/%{_lib}/libgcrypt.so
/usr/share/aclocal/libgcrypt.m4

%changelog
* Thu Sep 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.6-1
- Initial version
