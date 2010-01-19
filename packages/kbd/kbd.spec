Summary: kbd
Name: kbd
Version: 1.15
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://freshmeat.net/projects/kbd
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-backspace-1.patch

Requires: base-layout, glibc

%description
The kbd package contains keytable files and keyboard utilities

%prep
%setup -q
%patch -p1

%build
./configure --prefix=/usr --datadir=/%{_lib}/kbd
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/%{_lib}/kbd
/usr/bin/chvt
/usr/bin/deallocvt
/usr/bin/dumpkeys
/usr/bin/fgconsole
/usr/bin/getkeycodes
/usr/bin/kbd_mode
/usr/bin/kbdrate
/usr/bin/loadkeys
/usr/bin/loadunimap
/usr/bin/mapscrn
/usr/bin/openvt
/usr/bin/psfaddtable
/usr/bin/psfgettable
/usr/bin/psfstriptable
/usr/bin/psfxtable
/usr/bin/setfont
/usr/bin/setkeycodes
/usr/bin/setleds
/usr/bin/setmetamode
/usr/bin/showconsolefont
/usr/bin/showkey
/usr/bin/unicode_start
/usr/bin/unicode_stop
/usr/share/man/man1/chvt.1
/usr/share/man/man1/deallocvt.1
/usr/share/man/man1/dumpkeys.1
/usr/share/man/man1/fgconsole.1
/usr/share/man/man1/kbd_mode.1
/usr/share/man/man1/loadkeys.1
/usr/share/man/man1/openvt.1
/usr/share/man/man1/psfaddtable.1
/usr/share/man/man1/psfgettable.1
/usr/share/man/man1/psfstriptable.1
/usr/share/man/man1/psfxtable.1
/usr/share/man/man1/setleds.1
/usr/share/man/man1/setmetamode.1
/usr/share/man/man1/showkey.1
/usr/share/man/man1/unicode_start.1
/usr/share/man/man1/unicode_stop.1
/usr/share/man/man5/keymaps.5
/usr/share/man/man8/getkeycodes.8
/usr/share/man/man8/kbdrate.8
/usr/share/man/man8/loadunimap.8
/usr/share/man/man8/mapscrn.8
/usr/share/man/man8/resizecons.8
/usr/share/man/man8/setfont.8
/usr/share/man/man8/setkeycodes.8
/usr/share/man/man8/showconsolefont.8
%ifarch i686
/usr/bin/resizecons
%endif

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
