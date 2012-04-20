Summary: popt
Name: popt
Version: 1.16
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://rpm5.org/files/popt
Source0: http://rpm5.org/files/popt/popt-1.16.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = cfe94a15a2404db85858a81ff8de27c8ff3e235e

%description
The popt library exists essentially for parsing command line options.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
./configure \
  --prefix='' \
  --disable-shared
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
/include/popt.h
/lib/libpopt.a
/lib/libpopt.la
/lib/pkgconfig/popt.pc
/share/man/man3/popt.3.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.16-1
- Initial version
