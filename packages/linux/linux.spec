Summary: The Linux Kernel
Name: linux
Version: 2.6.33.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
%ifarch x86_64
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}-configs/%{name}-config-%{version}-x86_64
BuildRequires: digest(%{SOURCE1}) = 367662fc75245ca343016c8f04e4e387
%endif

Requires: base-layout
BuildRequires: digest(%{SOURCE0}) = 80c5ff544b0ee4d9b5d8b8b89d4a0ef9

%description
The Linux Kernel

%package headers
Group: Development
Summary: Linux Userspace Headers

%description headers
In order to compile anything, the Linux kernel needs to expose an
Application Programming Interface (API) for the system's C library (Glibc)
to utilize. This is done by sanitizing various C header files that are
shipped in the Linux kernel source package.

%prep
%setup -q

%build
make mrproper
make headers_install
make headers_check
make INSTALL_HDR_PATH=dest headers_install
find dest -name .install -exec rm -v '{}' \;
find dest -name ..install.cmd -exec rm -v '{}' \;
cp %{SOURCE1} .config
make

%install
mkdir -pv %{buildroot}/usr/include
cp -rv dest/include/* %{buildroot}/usr/include
mkdir %{buildroot}/boot
%ifarch x86_64
cp arch/x86_64/boot/bzImage %{buildroot}/boot/%{name}-%{version}-%{release}
%endif
cp System.map %{buildroot}/boot/System.map-%{version}-%{release}
cp .config %{buildroot}/boot/config-%{version}-%{release}
make INSTALL_MOD_PATH=%{buildroot} modules_install

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
/boot/System.map-%{version}-%{release}
/boot/config-%{version}-%{release}
/boot/linux-%{version}-%{release}
/lib/firmware
/lib/modules/%{version}

%files headers
%defattr(-,root,root)
/usr/include/asm
/usr/include/asm-generic
/usr/include/drm
/usr/include/linux
/usr/include/mtd
/usr/include/rdma
/usr/include/scsi
/usr/include/sound
/usr/include/video
/usr/include/xen

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.33.2-1
- Upgrade to 2.6.33.2, add in kernel image

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.6.31.4

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
