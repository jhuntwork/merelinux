Summary: Linux-PAM (Pluggable Authentication Modules for Linux)
Name: Linux-PAM
Version: 1.1.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://fedorahosted.org/linux-pam
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: https://raw.github.com/jhuntwork/LightCube-OS/musl/packages/Linux-PAM/no-innetgr.patch
Patch1: https://raw.github.com/jhuntwork/LightCube-OS/musl/packages/Linux-PAM/fix_ruserok.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 4634b09f9e059f384ce69dbaa4a67f88bef5cf7b
BuildRequires: digest(sha1:%{PATCH0})  = d95dbffcaf5de91e732c43f926be895ae8a54b20
BuildRequires: digest(sha1:%{PATCH1})  = cf4a40db8d2a9fbc172fc8120f8b01d40f5beccd
BuildRequires: db-devel
BuildRequires: flex-devel
BuildRequires: zlib-devel

%description
Linux-PAM (Pluggable Authentication Modules for Linux) is a suite of shared
libraries that enable the local system administrator to choose how
applications authenticate users.

%package devel
Summary: Libraries, headers and documentation for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%description devel
Libaries, headers and documentation for developing with %{name}

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{config_musl}
# include sys/types.h 
sed -i "/pam_types\.h/s@.*@#include <sys/types.h>\n&@" \
  libpam/include/security/pam_modutil.h
# strdupa is glibc specific
sed -i "75 s@.*@#define strdupa(x) strcpy(alloca(strlen((x))+1),(x))\n@" \
  modules/pam_exec/pam_exec.c
# No lastlog struct defined by system
sed -i "41 s@.*@& || !defined(_LASTLOG_H)\n#include <paths.h>\n#define UT_HOSTSIZE	256\n#define UT_NAMESIZE	32@" \
  modules/pam_lastlog/pam_lastlog.c
# No logwtmp provided - just comment it out for the time being
sed -i '/logwtmp/s@.*@/\* & \*/@' modules/pam_lastlog/pam_lastlog.c
# Don't use crypt_r
sed -i '/HAVE_CRYPT_R/s@.*@#if defined(HAVE_CRYPT_R) \&\& defined(HAVE_CRYPT_H)@' \
  modules/pam_pwhistory/opasswd.c modules/pam_unix/bigcrypt.c modules/pam_unix/passverify.c
sed -i 's/@LIBCRYPT@/-lcrypt/' \
  modules/pam_pwhistory/Makefile.in \
  modules/pam_unix/Makefile.in \
  modules/pam_userdb/Makefile.in
# Enable functionality in pam_rhosts.c
sed -i \
  -e "/syslog\.h/s@.*@&\n#include <unistd.h>\n#include <stdlib.h>\n#include <ctype.h>\n#include <arpa/inet.h>@" \
  -e 's@__UCLIBC__@MUSL@g' \
  -e "47 s@.*@#include <netinet/in.h>\n#define	_PATH_HEQUIV	\"/etc/hosts.equiv\"@" \
  modules/pam_rhosts/pam_rhosts.c
# Add unistd.h to bigcrypt.c
sed -i "/config\.h/s@.*@&\n#include <unistd.h>@" modules/pam_unix/bigcrypt.c
# Don't update /etc/passwd or /etc/shadow - not your job :)
sed -i -e '794,798d' -e '906,926d' -e '940,943d' \
  modules/pam_unix/passverify.c

%build
export CFLAGS='-g -D_GNU_SOURCE -DSYSLOG_NAMES -Os -pipe -Werror=implicit-function-declaration -DMUSL'
export LDFLAGS='-g'
./configure \
  --docdir=/usr/share/doc/%{name}-%{version} \
  --libdir=/lib \
  --sbindir=/lib/security \
  --enable-read-both-confs
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/pam.d
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /etc/environment
%dir /etc/pam.d
/etc/security
/lib/libpam.so.0
/lib/libpam.so.0.83.1
/lib/libpam_misc.so.0
/lib/libpam_misc.so.0.82.0
/lib/libpamc.so.0
/lib/libpamc.so.0.82.1
/lib/security

%files extras
%defattr(-,root,root)
/usr/share/doc/%{name}-%{version}
/usr/share/man/man3/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/lib/libpamc.so
/lib/libpam_misc.so
/lib/libpam.so
/lib/libpam.la
/lib/libpam_misc.la
/lib/libpamc.la
/usr/include/security

%changelog
* Thu Jan 26 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.4-3
- Initial version
