Summary: module-init-tools
Name: module-init-tools
Version: 3.12
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/kernel/module-init-tools
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(%{SOURCE0}) = 8b2257ce9abef74c4a44d825d23140f3
BuildRequires: zlib-devel

%description
Tools for activating Linux kernel modules

%prep
%setup -q

%build
# As per LFS instructiosn - avoid regenerating man pages
echo '.so man5/modprobe.conf.5' > modprobe.d.5
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/ \
  --enable-zlib-dynamic \
  --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} INSTALL=install install
install -dv %{buildroot}/etc/modprobe.d
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/lsmod
/etc/modprobe.d
/sbin/depmod
/sbin/insmod
/sbin/insmod.static
/sbin/modinfo
/sbin/modprobe
/sbin/rmmod
/usr/share/man/man5/depmod.conf.5.bz2
/usr/share/man/man5/modprobe.conf.5.bz2
/usr/share/man/man5/modprobe.d.5.bz2
/usr/share/man/man5/modules.dep.5.bz2
/usr/share/man/man8/depmod.8.bz2
/usr/share/man/man8/insmod.8.bz2
/usr/share/man/man8/lsmod.8.bz2
/usr/share/man/man8/modinfo.8.bz2
/usr/share/man/man8/modprobe.8.bz2
/usr/share/man/man8/rmmod.8.bz2

%changelog
* Tue Sep 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.12-3
- Add an /etc/modprobe.d directory

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.12-2
- Fix rogue info file instructions

* Tue Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.12-1
- Upgrade to 3.12

* Tue Dec 29 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.11.1-1
- Upgrade to 3.11.1

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.10-2
- Use FHS compatible info directories

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.10-1
- Initial version
