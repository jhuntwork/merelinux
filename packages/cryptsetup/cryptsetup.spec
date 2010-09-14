Summary: cryptsetup
Name: cryptsetup
Version: 1.1.3
Release: 1
Group: Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://code.google.com/p/cryptsetup
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 6f8a4c9a80a0d25f8492dfce6db6abed221598f6
BuildRequires: util-linux-ng-devel
BuildRequires: LVM2-libdevmapper-devel
BuildRequires: libgcrypt-devel
BuildRequires: popt-devel
BuildRequires: libgpg-error-devel

%description
Setup virtual encryption devices under dm-crypt Linux.

%package devel
Summary: Headers and Libraries for developing with cryptsetup
Group: Development/Libraries
Requires: %{name} = %{version}

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --sysconfdir=/etc \
  --sbindir=/sbin
make

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{find_lang} %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/sbin/cryptsetup
/usr/%{_lib}/libcryptsetup.so.1
/usr/%{_lib}/libcryptsetup.so.1.0.0
/usr/share/man/man8/cryptsetup.8.bz2

%files devel
%defattr(-,root,root)
/usr/include/libcryptsetup.h
/usr/%{_lib}/libcryptsetup.la
/usr/%{_lib}/libcryptsetup.so
/usr/%{_lib}/pkgconfig/libcryptsetup.pc

%changelog
* Tue Sep 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.3-1
- Initial version
