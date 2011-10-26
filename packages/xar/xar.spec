Summary: The eXtensible ARchive format
Name: xar
Version: 1.5.2
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://code.google.com/p/xar
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = eb411a92167387aa5d06a81970f7e929ec3087c9
BuildRequires: libxml2-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: bzip2-devel

%description
Xar provides a utility for manipulating files in XAR format.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS='-Os -s'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/xar
/usr/%{_lib}/libxar.so.1
/usr/share/man/man1/xar.1.bz2

%files devel
%defattr(-,root,root)
/usr/include/xar
/usr/%{_lib}/libxar.a
/usr/%{_lib}/libxar.la
/usr/%{_lib}/libxar.so

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5.2-2
- Optimize for size

* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5.2-1
- Initial version
