Summary: Fine Free File Command
Name: file
Version: 5.09
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://darwinsys.com/file
Source0: ftp://ftp.astron.com/pub/file/file-5.09.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 9d905f9e50033c3f5be3728473cbb709a41550fb
BuildRequires: zlib-devel

%description
The file command is "a file type guesser", that is, a command-line tool that
tells you in words what kind of data a file contains. It does not rely on
filename extensions, but looks at the contents of a file to determine its type.

%package devel
Summary: Libraries and headers for developing with libmagic
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with libmagic

%prep
%setup -q
%{config_musl}
# Move the datadir location from /share/misc to /share/file
sed -i 's/misc/file/' configure
sed -i '/memory.h/d' src/ascmagic.c src/encoding.c

%build
export CFLAGS='-D_GNU_SOURCE -Os'
export LDFLAGS="--static"
./configure \
  --prefix='' \
  --disable-shared 
make V=1 %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/file
/share/file
/share/man/man1/file.1.bz2
/share/man/man4/magic.4.bz2

%files devel
%defattr(-,root,root)
/include/magic.h
/lib/libmagic.a
/lib/libmagic.la
/share/man/man3/libmagic.3.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.09-1
- Initial version
