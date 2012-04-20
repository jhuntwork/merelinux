Summary: GNU Debugger
Name: gdb
Version: 7.4
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gdb/
Source0: http://ftp.gnu.org/gnu/gdb/%{name}-%{version}.tar.bz2
Patch0: https://raw.github.com/rofl0r/sabotage/master/KEEP/gdb-linux_nat.patch
Patch1: https://raw.github.com/rofl0r/sabotage/master/KEEP/gdb-amd64-debugreg.patch
Patch2: https://raw.github.com/rofl0r/sabotage/master/KEEP/gdb-linux_threaddb.patch
Patch3: https://raw.github.com/rofl0r/sabotage/master/KEEP/gdb-disable_dlopen.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 43a3ee582eae4d69c2babea4f8700b7bec8e37fa
BuildRequires: ncurses-devel

%description
GDB, the GNU Project debugger, allows you to see what is going on 'inside'
another program while it executes -- or what another program was doing at the
moment it crashed.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{config_musl}
# Don't bail on missing makeinfo
sed -i '7199 s@.*@MAKEINFO="true"@' gdb/configure

%build
export CFLAGS="-g -DHAVE_DECL_BASENAME -D_GNU_SOURCE -DUT_NAMESIZE=32 -Os -pipe"
export LDFLAGS="-g"
./configure \
  --prefix=/usr \
  --disable-nls \
  --disable-werror \
  --disable-tls \
  --enable-gdbserver=no
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/info
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/gdb
/usr/bin/gdbtui

%files extras
%defattr(-,root,root)
/usr/lib/libbfd.a
/usr/lib/libbfd.la
/usr/lib/libiberty.a
/usr/lib/libopcodes.a
/usr/lib/libopcodes.la
/usr/include/ansidecl.h
/usr/include/bfd.h
/usr/include/bfdlink.h
/usr/include/dis-asm.h
/usr/include/gdb
/usr/include/symcat.h
/usr/share/gdb
/usr/share/man/man1/gdb.1.bz2
/usr/share/man/man1/gdbtui.1.bz2

%changelog
* Tue Feb 07 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.4-1
- Initial version
