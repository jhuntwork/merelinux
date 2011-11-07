Summary: GNU Bash
Name: bash
Version: 4.2
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bash
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/bash/bashrc
Source2: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/bash/profile
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-rpm_requires-1.patch
Patch1: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-001
Patch2: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-002
Patch3: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-003
Patch4: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-004
Patch5: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-005
Patch6: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-006
Patch7: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-007
Patch8: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-008
Patch9: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-009
Patch10: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-010

BuildRequires: digest(sha1:%{SOURCE0}) = 487840ab7134eb7901fbb2e49b0ee3d22de15cb8
BuildRequires: digest(sha1:%{SOURCE1}) = a8b324e7dbf7f60492dda2fbd80f4811bd213a8d
BuildRequires: digest(sha1:%{SOURCE2}) = 8dfff5981a53efde15591b4383734a1c0f285d1a 
BuildRequires: digest(sha1:%{PATCH0})  = b84164630c0c1353730cc8695d0d49304bcb8141
BuildRequires: digest(sha1:%{PATCH1})  = c069f07492c9199bc7cff71a4f032f668ba4ea0a
BuildRequires: digest(sha1:%{PATCH2})  = 75b6726656a08e47172704545c57a290e29075e9
BuildRequires: digest(sha1:%{PATCH3})  = c18390edcc87c347cade67d9c1653f1f220ce64d
BuildRequires: digest(sha1:%{PATCH4})  = e10f0e8d3c24c10efffbca4605acb966393901ff
BuildRequires: digest(sha1:%{PATCH5})  = c1dd32f9aab963830cb9bf5c0973eefa4d7f8881
BuildRequires: digest(sha1:%{PATCH6})  = 4ae28b47a46850db3a5936ff0fafb9056f15329f
BuildRequires: digest(sha1:%{PATCH7})  = 31cf0373b1d4d61540474b6f527bf7675e8773f3
BuildRequires: digest(sha1:%{PATCH8})  = 7f0961aaf284b36eac1503824cd9e85926628120
BuildRequires: digest(sha1:%{PATCH9})  = c7f9dede34e30494a9adb479e406814f4d62da2a
BuildRequires: digest(sha1:%{PATCH10}) = 662192c4675300f488897a6ed8774e16e7a13e2e
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: shadow

%description
Bash is an sh-compatible shell that incorporates useful features from the
Korn shell (ksh) and C shell (csh).

%prep
%setup -q
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
%patch5 -p0
%patch6 -p0
%patch7 -p0
%patch8 -p0
%patch9 -p0
%patch10 -p0

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --bindir=/bin \
  --without-bash-malloc \
  --htmldir=/usr/share/doc/%{name}-%{version} \
  --with-installed-readline
make %{PMFLAGS}
chown -Rv nobody ./
su nobody -s /bin/bash -c "make tests"

%install
make DESTDIR=%{buildroot} install
ln -vs bash %{buildroot}/bin/sh
install -dv %{buildroot}/etc
install -m 0644 %{SOURCE1} %{buildroot}/etc/
install -m 0644 %{SOURCE2} %{buildroot}/etc/
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/bash.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/bash.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/bin/bash
/bin/bashbug
/bin/sh
%config /etc/bashrc
%config /etc/profile
/usr/share/doc/%{name}-%{version}
/usr/share/info/bash.info
/usr/share/man/man1/bash.1.bz2
/usr/share/man/man1/bashbug.1.bz2

%changelog
* Fri May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2-3
- Optimize for size
- Merge doc package back into main

* Fri May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2-2
- Add some upstream fixes, and properly link against ncurses

* Fri Mar 04 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2-1
- Upgrade to 4.2

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-6
- Properly identify config files

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-5
- Add HISTSIZE and HISTTIMEFORMAT default values to /etc/profile

* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-4
- Updated bash rpm-requires patch and upstream patch

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-3
- Add in user environment files, fix build dependencies

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-2
- Add in upstream patches

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-1
- Uppdated to 4.1

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-3
- Use FHS compatible info directories

* Thu Sep 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-2
- Updated upstream patches

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-1
- Initial version
