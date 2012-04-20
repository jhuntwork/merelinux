Summary: initd-tools
Name: initd-tools
Version: 0.1.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.dwcab.com/projects/initd-tools
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: initd-tools-while_fix.patch
Patch1: initd-tools-no_error.patch
Patch2: initd-tools-no_program_invocation_name.patch
Patch3: initd-tools-gcwd.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 2d09b0c2cb4b0727e9d2c64534038a483c69350a
BuildRequires: digest(sha1:%{PATCH0})  = 6f93e77540d2e212cbabb2236374dbdc51b31447
BuildRequires: digest(sha1:%{PATCH1})  = d1e8014421d8d9af7123085495a2e97cdd877781
BuildRequires: digest(sha1:%{PATCH2})  = 33f91cc78a1fbee76d3d70a6ab1afd63a4b41cdc
BuildRequires: digest(sha1:%{PATCH3})  = abb31872e55f6006857cac888c1ed3a60918dec0

%description
initd-tools is an implementation of the init script installation and removal
programs in Linux Standard Base (LSB) 3.2 specification.

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

%build
./configure
sed -i '/^CFLAGS/s@=.*@= -D_GNU_SOURCE -DNO_GET_CURRENT_DIR_NAME -Os -pipe@' Makefile src/Makefile lib/Makefile
make
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/lsb/install_initd
/usr/lib/lsb/remove_initd
/usr/sbin/install_initd
/usr/sbin/remove_initd

%files extras
/usr/share/man/man8/install_initd.8.bz2
/usr/share/man/man8/remove_initd.8.bz2

%changelog
* Wed Feb 01 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1.3-1
- Initial version
