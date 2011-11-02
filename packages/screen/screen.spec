Summary: GNU Screen
Name: screen
Version: 4.0.3
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/screen
Source0: http://ftp.gnu.org/gnu/screen/screen-4.0.3.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 7bc6e2f0959ffaae6f52d698c26c774e7dec3545
BuildRequires: ncurses-devel

%description
Screen is a full-screen window manager that multiplexes a physical terminal
between several processes, typically interactive shells.

%prep
%setup -q

%build
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --with-sys-screenrc=/etc/screenrc \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man 
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc
# Default configurations:
cat > %{buildroot}/etc/screenrc << "EOF"
# use a login shell
shell -$SHELL
# don't display the startup message
startup_message off
# scrollback lines
defscrollback 1000
EOF
%{compress_man}
%{strip}
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/screen.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/screen.info /usr/share/info/dir

%files
%defattr(-,root,root)
%config /etc/screenrc
/usr/bin/screen
/usr/bin/screen-4.0.3
/usr/share/screen
/usr/share/info/screen.info
/usr/share/info/screen.info-1
/usr/share/info/screen.info-2
/usr/share/info/screen.info-3
/usr/share/info/screen.info-4
/usr/share/info/screen.info-5
/usr/share/man/man1/screen.1.bz2

%changelog
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0.3-2
- Optimize for size

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0.3-1
- Initial version
