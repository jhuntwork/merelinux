Summary: module-init-tools
Name: module-init-tools
Version: 3.15
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools
Source0: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools/module-init-tools-3.15.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = d044d4c737e92e9167a5cc015429af2ce3b57da9
BuildRequires: zlib-devel

%description
Tools for activating Linux kernel modules

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}

%build
export CFLAGS="-Os -pipe"
DOCBOOKTOMAN=/bin/true ./configure \
  --prefix=/ \
  --enable-zlib-dynamic \
  --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} INSTALL=install install
install -dv %{buildroot}/etc/modprobe.d
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/lsmod
%dir /etc/modprobe.d
/sbin/depmod
/sbin/insmod
/sbin/insmod.static
/sbin/modinfo
/sbin/modprobe
/sbin/rmmod

%files extras
%defattr(-,root,root)
/usr/share/man/man5/depmod.conf.5.bz2
/usr/share/man/man5/depmod.d.5.bz2
/usr/share/man/man5/modprobe.conf.5.bz2
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
* Wed Feb 01 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.15-1
- Initial version
