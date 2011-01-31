Summary: udev
Name: udev
Version: 165
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/utils/kernel/hotplug/udev.html
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 1dab9e274723d6a142a38227de3b52c030abbf07
BuildRequires: xsltproc

%description
Udev provides a dynamic /dev directory, and hooks userspace into kernel device events.

%package devel
Requires: %{name}

%description devel
Files for developing with %{name}

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --sbindir=/sbin \
  --with-rootlibdir=/%{_lib} \
  --libexecdir=/lib/udev \
  --disable-extras \
  --libdir=/usr/%{_lib} \
  --disable-introspection \
  --with-html-dir=/usr/share/doc/%{name}
make

%install
install -dv %{buildroot}/lib/udev/devices/{pts,shm}
make DESTDIR=%{buildroot} install
sed -i 's@include$@&\nudevdir=/lib/udev@' %{buildroot}/usr/%{_lib}/pkgconfig/libudev.pc
mknod -m0666 %{buildroot}/lib/udev/devices/null c 1 3
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/udev
/%{_lib}/libudev.so.*
/lib/udev
/sbin/udevadm
/sbin/udevd
/usr/share/man/man7/udev.7.bz2
/usr/share/man/man8/scsi_id.8.bz2
/usr/share/man/man8/udevadm.8.bz2
/usr/share/man/man8/udevd.8.bz2

%files devel
%defattr(-,root,root)
/usr/include/libudev.h
/usr/%{_lib}/libudev.so
/usr/%{_lib}/libudev.la
/usr/%{_lib}/pkgconfig/libudev.pc
/usr/share/pkgconfig/udev.pc
/usr/share/doc/udev

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 165-1
- Upgrade to 165

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 160-1
- Upgrade to 160

* Sat Apr 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 151-1
- Initial version
