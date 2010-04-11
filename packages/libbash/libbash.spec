Summary: libbash
Name: libbash
Version: 0.9.11
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://sourceforge.net/projects/libbash
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 4588941de6547e09aac595474f01c2ba

%description
libbash is a tool that enables bash dynamic-like shared libraries.
It is a tool for managing bash scripts that contain functions you may want to
use in various scripts.

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib} --sysconfdir=/etc
make

%install
make DESTDIR=%{buildroot} install
touch %{buildroot}/etc/ldbash.cache

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/ldbash.cache
/usr/bin/ldbash
/usr/%{_lib}/bash
/usr/sbin/ldbashconfig
/usr/share/aclocal/libbash.m4
/usr/share/man/man1/getopt_long.1
/usr/share/man/man1/ldbash.1
/usr/share/man/man3/colorPrint.3
/usr/share/man/man3/colorPrintN.3
/usr/share/man/man3/colorReset.3
/usr/share/man/man3/colorSet.3
/usr/share/man/man3/colors.3
/usr/share/man/man3/dirDestroyLock.3
/usr/share/man/man3/dirInitLock.3
/usr/share/man/man3/dirLock.3
/usr/share/man/man3/dirTryLock.3
/usr/share/man/man3/dirUnlock.3
/usr/share/man/man3/getopts.3
/usr/share/man/man3/hashDelete.3
/usr/share/man/man3/hashGet.3
/usr/share/man/man3/hashKeys.3
/usr/share/man/man3/hashRemove.3
/usr/share/man/man3/hashSet.3
/usr/share/man/man3/hashstash.3
/usr/share/man/man3/locks.3
/usr/share/man/man3/messages.3
/usr/share/man/man3/printATTN.3
/usr/share/man/man3/printFAIL.3
/usr/share/man/man3/printNA.3
/usr/share/man/man3/printOK.3
/usr/share/man/man3/printWAIT.3
/usr/share/man/man3/urlcoding.3
/usr/share/man/man7/libbash.7
/usr/share/man/man8/ldbashconfig.8

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.9.11-1
- Initial version
