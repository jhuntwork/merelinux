Summary: libvirt Virtualization API
Name: libvirt
Version: 0.8.7
Release: 1
Group: Virtualization
License: GPL
Distribution: Critical OS
Vendor: Critical Mention
URL: http://libvirt.org
Source0: http://os.criticalmention.com/pub/sources/%{name}/%{name}-%{version}.tar.gz

Requires: logrotate
BuildRequires: digest(sha1:%{SOURCE0}) = 53b10513cb04c502a2c8aaf57039c71f0f79ea6f
BuildRequires: openssl-devel
BuildRequires: readline-devel
BuildRequires: libxml2-devel
BuildRequires: gnutls-devel
BuildRequires: LVM2-libdevmapper-devel
BuildRequires: curl-devel
BuildRequires: parted-devel
BuildRequires: libgcrypt-devel
BuildRequires: libgpg-error-devel
BuildRequires: xen-devel
BuildRequires: udev-devel
BuildRequires: Python-devel
BuildRequires: util-linux-ng-devel
BuildRequires: zlib-devel

%description
A toolkit to interact with the virtualization capabilities of recent versions
of Linux (and other OSes).

%package python
Summary: Libraries for using libvirt with Python
Group: Development/Libraries
Requires: Python, libvirt >= %{version}

%description python
Libraries for using libvirt with Python

%package devel
Summary: Headers and libraries for developing with libvirt
Group: Development/Libraries
Requires: libvirt >= %{version}

%description devel
Headers and libraries for developing with libvirt

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/lib/libvirt \
  --without-macvtap \
  --with-xen \
  --without-qemu

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/gtk-doc
%{find_lang} %{name}
%{compress_man}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/libvirt
%config /etc/libvirt/libvirtd.conf
%config /etc/libvirt/lxc.conf
/etc/libvirt/nwfilter
/etc/libvirt/qemu
/etc/logrotate.d/libvirtd.lxc
/etc/logrotate.d/libvirtd.qemu
/etc/logrotate.d/libvirtd.uml
/usr/bin/virsh
/usr/bin/virt-pki-validate
/usr/bin/virt-xml-validate
/usr/%{_lib}/libvirt-qemu.so.*
/usr/%{_lib}/libvirt.so.*
/usr/lib/libvirt
/usr/sbin/libvirtd
/usr/share/augeas
/usr/share/doc/libvirt-%{version}/
/usr/share/libvirt
/usr/share/man/man1/virsh.1.bz2
/usr/share/man/man1/virt-pki-validate.1.bz2
/usr/share/man/man1/virt-xml-validate.1.bz2
/usr/share/man/man8/libvirtd.8.bz2

%files python
%defattr (-,root,root)
/usr/lib/python2.7/site-packages/libvirt.py
/usr/lib/python2.7/site-packages/libvirtmod.la
/usr/lib/python2.7/site-packages/libvirtmod.so
/usr/share/doc/libvirt-python-%{version}

%files devel
%defattr (-,root,root)
/usr/include/libvirt
/usr/%{_lib}/libvirt-qemu.a
/usr/%{_lib}/libvirt-qemu.la
/usr/%{_lib}/libvirt-qemu.so
/usr/%{_lib}/libvirt.a
/usr/%{_lib}/libvirt.la
/usr/%{_lib}/libvirt.so
/usr/%{_lib}/pkgconfig/libvirt.pc

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@criticalmention.com> - 0.8.7-1
- Initial version
