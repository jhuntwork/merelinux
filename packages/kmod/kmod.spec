Summary: kmod - handle kernel modules
Name: kmod
Version: 5
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://git.profusion.mobi/cgit.cgi/kmod.git
Source0: http://packages.profusion.mobi/kmod/kmod-%{version}.tar.xz 
Patch0: kmod-5-portability.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 415f3650c15d17324cbaae6fa6bf59381cb8cbb8
BuildRequires: digest(sha1:%{PATCH0})  = 89f8fcf1dbbf83bd74c6585123441ccbac18dc6e
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
kmod is a set of tools to handle common tasks with Linux kernel modules like
insert, remove, list, check properties, resolve dependencies and aliases.
These tools are designed on top of libkmod, a library that is shipped with
kmod. The aim is to be compatible with tools, configurations and indexes from
module-init-tools project.

%package devel
Summary: %{name} headers and libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

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
#sed -i 's@\*(.* \*\*)p@*p@' libkmod/libkmod-index.c
%{config_musl}

%build
export CFLAGS="-Os -pipe -D_GNU_SOURCE -Wall -DNO_GET_CURRENT_DIR_NAME -DMAP_POPULATE=0x8000 -Werror=implicit-function-declaration"
./configure \
  --prefix=/usr \
  --bindir=/bin \
  --libdir=/lib \
  --sysconfdir=/etc \
  --with-xz \
  --with-zlib
make V=1 %{PMFLAGS}

%install
make pkgconfigdir=/usr/lib/pkgconfig DESTDIR=%{buildroot} install
install -d %{buildroot}/etc/modprobe.d
install -d %{buildroot}/sbin
for file in depmod insmod lsmod modinfo modprobe rmmod ; do
  ln -s ../bin/kmod %{buildroot}/sbin/$file
done
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/kmod
%dir /etc/modprobe.d
/lib/libkmod.so.2
/lib/libkmod.so.2.0.0
/sbin/depmod
/sbin/insmod
/sbin/lsmod
/sbin/modinfo
/sbin/modprobe
/sbin/rmmod

%files devel
%defattr(-,root,root)
/lib/libkmod.la
/lib/libkmod.so
/usr/lib/pkgconfig/libkmod.pc
/usr/include/libkmod.h

%files extras
%defattr(-,root,root)
/usr/share/man/man5/depmod.d.5.bz2
/usr/share/man/man5/modprobe.d.5.bz2
/usr/share/man/man5/modules.dep.5.bz2
/usr/share/man/man5/modules.dep.bin.5.bz2
/usr/share/man/man8/depmod.8.bz2
/usr/share/man/man8/insmod.8.bz2
/usr/share/man/man8/lsmod.8.bz2
/usr/share/man/man8/modinfo.8.bz2
/usr/share/man/man8/modprobe.8.bz2
/usr/share/man/man8/rmmod.8.bz2

%changelog
* Wed Feb 01 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4-1
- Initial version
