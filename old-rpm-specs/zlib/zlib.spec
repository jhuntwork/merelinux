Summary: zlib Compression Library
Name: zlib
Version: 1.2.6
Release: 1
Group: System Environment/Libraries
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.zlib.net
Source0: http://zlib.net/zlib-1.2.6.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 3d445731e4bfea1cd00f36567d77d6e5f5a19be9

%description
According to its maintainers, zlib is:
A Massively Spiffy Yet Delicately Unobtrusive Compression Library

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q
# Busybox doesn't support mktemp -u
sed -i 's@mktemp -u@mktemp@' Makefile.in

%build
export CFLAGS="-Os -pipe -fPIC"
./configure \
  --prefix='' \
  --static
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
/lib/libz.a
/lib/pkgconfig/zlib.pc
/share/man/man3/zlib.3.bz2
/include/zconf.h
/include/zlib.h

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 1.2.6-1
- Initial version
