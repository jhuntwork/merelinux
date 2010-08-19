Summary: psmisc
Name: psmisc
Version: 22.12
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://psmisc.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, ncurses
BuildRequires: digest(%{SOURCE0}) = 16c83a351c292cfc845b27d6395e05fb
BuildRequires: digest(%{PATCH0}) = 13c8659fcdfa32490e5a02fb53074b25
BuildRequires: ncurses-devel

%description
The PSmisc package is a set of some small useful utilities that use the proc filesystem.

%prep
%setup -q
%ifarch x86_64
sed -i 's@#include <sys\/user.h>@#include <bits\/types.h>\n&@' configure
%endif

%build
./configure --prefix=/usr --exec-prefix=""
make

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/bin
mv -v %{buildroot}/bin/pstree* %{buildroot}/usr/bin
rm -vf %{buildroot}/usr/bin/pstree.x11
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/fuser
/bin/killall
/bin/peekfd
/bin/prtstat
/usr/bin/pstree
/usr/share/man/man1/fuser.1
/usr/share/man/man1/killall.1
/usr/share/man/man1/peekfd.1
/usr/share/man/man1/prtstat.1
/usr/share/man/man1/pstree.1

%changelog
* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.12-1
- Upgrade to 22.12

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.10-2
- Remove pidof since sysvinit provides a better one

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.10-1
- Upgrade to 22.10

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
