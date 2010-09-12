Summary: The Linux Kernel
Name: linux
Version: 2.6.35.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout
BuildRequires: digest(sha1:%{SOURCE0}) = 60f4b0f178034a0629c5fcf75b79818b1feef0ed

%ifarch x86_64
Source1: http://dev.lightcube.us/sources/%{name}-configs/%{name}-config-%{version}-x86_64
BuildRequires: digest(sha1:%{SOURCE1}) = 1097637e5829eae09bc3bed288aa7d1ad7cf4c0f
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
# Install the headers
mkdir -pv %{buildroot}/usr/include
cp -rv dest/include/* %{buildroot}/usr/include

# Install the modules
make INSTALL_MOD_PATH=%{buildroot} modules_install

# Install the kernel source
DIRNAME="/usr/src/kernels/%{name}-%{version}-%{release}"
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
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}/source"
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}/build"

# Install the kernel image, system.map and config
mkdir %{buildroot}/boot
cp System.map %{buildroot}/boot/System.map-%{version}-%{release}
cp .config %{buildroot}/boot/config-%{version}-%{release}
%ifarch x86_64
cp arch/x86_64/boot/bzImage %{buildroot}/boot/vmlinux-%{version}-%{release}
%endif
%ifarch i686
cp arch/x86/boot/bzImage %{buildroot}/boot/vmlinux-%{version}-%{release}
%endif

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
/boot/System.map-%{version}-%{release}
/boot/config-%{version}-%{release}
/boot/vmlinux-%{version}-%{release}
/lib/firmware
%dir /lib/modules/%{version}
/lib/modules/%{version}/kernel
/lib/modules/%{version}/modules.*

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
/usr/src/kernels/%{name}-%{version}-%{release}
/lib/modules/%{version}/source
/lib/modules/%{version}/build

%changelog
* Mon Aug 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.35-1
- Upgrade to 2.6.35-1

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.33.2-1
- Upgrade to 2.6.33.2, add in kernel image

* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 2.6.31.4

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
