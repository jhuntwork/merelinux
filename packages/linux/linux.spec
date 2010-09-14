Summary: The Linux Kernel
Name: linux
Version: 2.6.36
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-rc4.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = d01857f41bd56d650d00003f4c69ba300924372f

%ifarch x86_64
Source1: http://dev.lightcube.us/sources/%{name}-configs/%{name}-config-%{version}-rc4.x86_64
BuildRequires: digest(sha1:%{SOURCE1}) = 191592b4cf48a8ab1799cf2d99e70e3c7139b0ee
%endif

%ifarch i686
Source1: http://dev.lightcube.us/sources/%{name}-configs/%{name}-config-%{version}-i686
BuildRequires: digest(%{SOURCE1}) = fc7cb3e55b3ee840166ba947918efbbc
%endif

%description
The Linux Kernel

%package headers
Group: Development
Summary: Linux Userspace Headers
Requires: base-layout

%description headers
In order to compile anything, the Linux kernel needs to expose an
Application Programming Interface (API) for the system's C library (Glibc)
to utilize. This is done by sanitizing various C header files that are
shipped in the Linux kernel source package.

%package devel
Group: Development/Kernel
Summary: Kernel sources for installed kernel
Requires: %{name}

%description devel
Kernel sources for installed kernel

%prep
%setup -q -n %{name}-%{version}-rc4

%build
make mrproper
make headers_install
make headers_check
make INSTALL_HDR_PATH=dest headers_install
find dest -name .install -exec rm -v '{}' \;
find dest -name ..install.cmd -exec rm -v '{}' \;
cp %{SOURCE1} .config
make -j8

%install
# Install the headers
mkdir -pv %{buildroot}/usr/include
cp -rv dest/include/* %{buildroot}/usr/include

# Install the modules
make INSTALL_MOD_PATH=%{buildroot} modules_install

# Install the kernel source
DIRNAME="/usr/src/kernels/%{name}-%{version}-rc4-%{release}"
install -dv "%{buildroot}$DIRNAME"
cp -a .config Module.symvers .version scripts include "%{buildroot}$DIRNAME"
install -dv "%{buildroot}$DIRNAME/arch/x86/"
cp -a arch/x86/include "%{buildroot}$DIRNAME/arch/x86/"
find . -type f -a '(' -name Kconfig\* -o -name Makefile\* -o -name \*.s ')' | (
  while read file
  do
    install -dv "%{buildroot}$DIRNAME/`dirname $file`"
    cp "$file" "%{buildroot}$DIRNAME/$file"
  done
)
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-rc4/source"
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-rc4/build"

# Install the kernel image, system.map and config
mkdir %{buildroot}/boot
cp System.map %{buildroot}/boot/System.map-%{version}-rc4-%{release}
cp .config %{buildroot}/boot/config-%{version}-rc4-%{release}
%ifarch x86_64
cp arch/x86_64/boot/bzImage %{buildroot}/boot/vmlinux-%{version}-rc4-%{release}
%endif
%ifarch i686
cp arch/x86/boot/bzImage %{buildroot}/boot/vmlinux-%{version}-rc4-%{release}
%endif

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
/boot/System.map-%{version}-rc4-%{release}
/boot/config-%{version}-rc4-%{release}
/boot/vmlinux-%{version}-rc4-%{release}
/lib/firmware
%dir /lib/modules/%{version}-rc4
/lib/modules/%{version}-rc4/kernel
/lib/modules/%{version}-rc4/modules.*

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

%files devel
%defattr(-,root,root)
/usr/src/kernels/%{name}-%{version}-rc4-%{release}
/lib/modules/%{version}-rc4/source
/lib/modules/%{version}-rc4/build

%changelog
* Mon Sep 13 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.36-rc4-1
- Upgrade to 2.6.36-rc4

* Mon Sep 13 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.35.4-2
- Upgrade to 2.6.35.4, add video4linux support

* Mon Aug 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.35-1
- Upgrade to 2.6.35-1

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.33.2-1
- Upgrade to 2.6.33.2, add in kernel image

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.6.31.4

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
