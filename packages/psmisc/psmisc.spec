Summary: psmisc
Name: psmisc
Version: 22.14
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://psmisc.sourceforge.net
Source0: http://iweb.dl.sourceforge.net/project/psmisc/psmisc/psmisc-22.14.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = dc6fc0ec131c11796d01512bbd80089719b04a66
BuildRequires: ncurses-devel

%description
The PSmisc package is a set of some small useful utilities that use the proc filesystem.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --exec-prefix=""
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/bin
mv -v %{buildroot}/bin/pstree* %{buildroot}/usr/bin
rm -vf %{buildroot}/usr/bin/pstree.x11
%{compress_man}
%{strip}
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
/usr/share/man/man1/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.14-1
- Upgrade to 22.14
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.13-1
- Upgrade to 22.13

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.12-1
- Upgrade to 22.12

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.10-2
- Remove pidof since sysvinit provides a better one

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.10-1
- Upgrade to 22.10

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
