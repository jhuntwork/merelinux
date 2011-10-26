Summary: pkg-config 
Name: pkg-config
Version: 0.25
Release: 2
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

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --with-pc-path=/usr/%{_lib}/pkgconfig
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}
install -dv %{buildroot}/usr/share/pkgconfig
install -dv %{buildroot}/usr/%{_lib}/pkgconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/pkg-config
/usr/share/aclocal/pkg.m4
%dir /usr/share/pkgconfig
%dir /usr/%{_lib}/pkgconfig
/usr/share/man/man1/pkg-config.1.bz2
/usr/share/doc/pkg-config

%changelog
* Tue Oct 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.25-2
- Optimize for size

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.25-1
- Upgrade to 0.25

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.23-1
- Initial version
