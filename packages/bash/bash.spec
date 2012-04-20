Summary: GNU Bash
Name: bash
Version: 4.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bash
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/musl/packages/bash/bashrc
Source2: https://raw.github.com/jhuntwork/LightCube-OS/musl/packages/bash/profile
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
Patch11: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-011
Patch12: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-012
Patch13: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-013
Patch14: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-014
Patch15: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-015
Patch16: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-016
Patch17: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-017
Patch18: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-018
Patch19: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-019
Patch20: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-020
Patch21: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-021
Patch22: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-022
Patch23: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-023
Patch24: http://ftp.gnu.org/gnu/bash/bash-4.2-patches/bash42-024

BuildRequires: digest(sha1:%{SOURCE0}) = 487840ab7134eb7901fbb2e49b0ee3d22de15cb8
BuildRequires: digest(sha1:%{SOURCE1}) = 399b8e1f00cb181a1c2643bd95c3e39faa1601ba
BuildRequires: digest(sha1:%{SOURCE2}) = 4d9c790af61a9af40187795dfa656c81855809ea
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
BuildRequires: digest(sha1:%{PATCH11}) = 5f4131f3ab9751a6828269ef4079a841258671cb
BuildRequires: digest(sha1:%{PATCH12}) = aad2483f7f48c29274ce0ef63027f3749b8388fc
BuildRequires: digest(sha1:%{PATCH13}) = 2d60fc3b0ee40f9eb308b76185142f865df0fa17
BuildRequires: digest(sha1:%{PATCH14}) = 320bba1f869602c07a9972862d38b9ba108726a6
BuildRequires: digest(sha1:%{PATCH15}) = 7b9c9a91ab5a79b8344877ff45ed204ba1b04ef3
BuildRequires: digest(sha1:%{PATCH16}) = f4a39fb2b79f7c5c04ee78fb598199ba7440fd70
BuildRequires: digest(sha1:%{PATCH17}) = f80797fce1fefff4047cecf0f32731bc30f6faee
BuildRequires: digest(sha1:%{PATCH18}) = 3624c31ed7d8c613b566e3d465480beed34bdaba
BuildRequires: digest(sha1:%{PATCH19}) = 21a75dadb1398775b48718e94785642f5fad9777
BuildRequires: digest(sha1:%{PATCH20}) = 5c4afeef6ef7321fcc5a08f2d3024c484868fa59
BuildRequires: digest(sha1:%{PATCH21}) = 55aabc84fdac1f3b26312f478fb9b7f14c81f2be
BuildRequires: digest(sha1:%{PATCH22}) = f2e7ff4050dce9ff5893cd027716caf22d17f369
BuildRequires: digest(sha1:%{PATCH23}) = 16224bc48c89df4dff22b8365e7d1d295f4adc9b
BuildRequires: digest(sha1:%{PATCH24}) = a78b4c48d0f372280ebe137b15bc3ef8807f7f8b
BuildRequires: ncurses-devel
BuildRequires: readline-devel

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
%patch11 -p0
%patch12 -p0
%patch13 -p0
%patch14 -p0
%patch15 -p0
%patch16 -p0
%patch17 -p0
%patch18 -p0
%patch19 -p0
%patch20 -p0
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
export LDFLAGS='--static'
./configure \
  --prefix=/ \
  --disable-nls \
  --without-bash-malloc \
  --with-installed-readline \
  ac_cv_func_mbsnrtowcs=no
make %{PMFLAGS}
#chown -Rv nobody ./
#su nobody -s /bin/bash -c "make tests"

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}/etc
install -m 0644 %{SOURCE1} %{buildroot}/etc/
install -m 0644 %{SOURCE2} %{buildroot}/etc/
rm -rf %{buildroot}/share/info
# Don't package bashbug for now
rm -f %{buildroot}/bin/bashbug
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/bash
%config /etc/bashrc
%config /etc/profile

%changelog
* Mon Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2-1
- Initial version
