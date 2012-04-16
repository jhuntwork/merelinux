Summary: pkg-config 
Name: pkg-config
Version: 0.25
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pkg-config.freedesktop.org
Source0: http://pkgconfig.freedesktop.org/releases/pkg-config-0.25.tar.gz
Provides: pkgconfig

BuildRequires: digest(sha1:%{SOURCE0}) = 8922aeb4edeff7ed554cc1969cbb4ad5a4e6b26e

%description
pkg-config is a helper tool used when compiling applications and libraries. It can
be used to determine library versions and compiler options needed for linking to
installed libraries.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --prefix='' \
  --with-pc-path=/lib/pkgconfig
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}
install -dv %{buildroot}/share/pkgconfig
install -dv %{buildroot}/lib/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/pkg-config
/share/aclocal/pkg.m4
%dir /lib/pkgconfig
%dir /share/pkgconfig
/share/man/man1/pkg-config.1.bz2

%files extras
%defattr(-,root,root)
/share/doc/pkg-config

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.25-1
- Initial version
