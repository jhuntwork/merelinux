Summary: kbd
Name: kbd
Version: 1.15.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://freshmeat.net/projects/kbd
#Source0: ftp://ftp.altlinux.org/pub/people/legion/kbd/kbd-1.15.3.tar.gz
# Using a snapshot from upstream with fixes for translation and loadkeys
Source0: http://dev.lightcube.us/sources/kbd/kbd-1.15.3-201110240419.tar.gz
Patch0: https://raw.github.com/jhuntwork/LightCube-OS/6a2885478a7d5fe7f80deccd15a58fd7f4085e3d/packages/kbd/backspace.patch

BuildRequires: digest(sha1:%{SOURCE0}) = a33b7afff7a32fe56b331406af98937d7f21ce21
BuildRequires: digest(sha1:%{PATCH0})  = 44f2fb0ac18db4f717421db756db4897f88dc08c

%description
The kbd package contains keytable files and keyboard utilities

%prep
%setup -q
%patch -p1

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --datadir=/lib/kbd
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/bin
mv -v %{buildroot}/usr/bin/{kbd_mode,loadkeys,openvt,setfont} %{buildroot}/bin
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/kbd_mode
/bin/loadkeys
/bin/openvt
/bin/setfont
/lib/kbd
/usr/bin/chvt
/usr/bin/deallocvt
/usr/bin/dumpkeys
/usr/bin/fgconsole
/usr/bin/getkeycodes
/usr/bin/kbdinfo
/usr/bin/kbdrate
/usr/bin/loadunimap
/usr/bin/mapscrn
/usr/bin/psfaddtable
/usr/bin/psfgettable
/usr/bin/psfstriptable
/usr/bin/psfxtable
/usr/bin/setkeycodes
/usr/bin/setleds
/usr/bin/setmetamode
/usr/bin/setvtrgb
/usr/bin/showconsolefont
/usr/bin/showkey
/usr/bin/unicode_start
/usr/bin/unicode_stop
/usr/share/man/man1/chvt.1.bz2
/usr/share/man/man1/deallocvt.1.bz2
/usr/share/man/man1/dumpkeys.1.bz2
/usr/share/man/man1/fgconsole.1.bz2
/usr/share/man/man1/kbd_mode.1.bz2
/usr/share/man/man1/loadkeys.1.bz2
/usr/share/man/man1/openvt.1.bz2
/usr/share/man/man1/psfaddtable.1.bz2
/usr/share/man/man1/psfgettable.1.bz2
/usr/share/man/man1/psfstriptable.1.bz2
/usr/share/man/man1/psfxtable.1.bz2
/usr/share/man/man1/setleds.1.bz2
/usr/share/man/man1/setmetamode.1.bz2
/usr/share/man/man1/showkey.1.bz2
/usr/share/man/man1/unicode_start.1.bz2
/usr/share/man/man1/unicode_stop.1.bz2
/usr/share/man/man5/keymaps.5.bz2
/usr/share/man/man8/getkeycodes.8.bz2
/usr/share/man/man8/kbdrate.8.bz2
/usr/share/man/man8/loadunimap.8.bz2
/usr/share/man/man8/mapscrn.8.bz2
/usr/share/man/man8/resizecons.8.bz2
/usr/share/man/man8/setfont.8.bz2
/usr/share/man/man8/setkeycodes.8.bz2
/usr/share/man/man8/setvtrgb.8.bz2
/usr/share/man/man8/showconsolefont.8.bz2

%changelog
* Thu Oct 27 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.15.3-1
- Upgrade to 1.15.3
- Optimize for size

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.15.2-1
- Upgrade to 1.15.2

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.15.1-1
- Upgrade to 1.15.1

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
