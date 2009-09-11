Summary: psmisc
Name: psmisc
Version: 22.8
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://psmisc.sourceforge.net
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc

%description
The PSmisc package is a set of some small useful utilities that use the proc filesystem.

%prep
%setup -q

%build
./configure --prefix=/usr --exec-prefix=""
make

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/bin
mv -v %{buildroot}/bin/pstree* %{buildroot}/usr/bin
ln -sv killall %{buildroot}/bin/pidof
rm -vf %{buildroot}/usr/bin/pstree.x11
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/fuser
/bin/killall
/bin/peekfd
/bin/pidof
/usr/bin/pstree
/usr/share/man/man1/fuser.1
/usr/share/man/man1/killall.1
/usr/share/man/man1/peekfd.1
/usr/share/man/man1/pstree.1

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
