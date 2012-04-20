Summary: The Linux Kernel
Name: linux
Version: 3.3.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://www.kernel.org/pub/linux/kernel/v3.0/%{name}-%{version}.tar.bz2
Source1: linux-config.x86_64
Patch0: linux-posix-sed.patch
Patch1: linux-noperl-timeconst.patch
Patch2: linux-noperl-capflags.patch

Requires(post): mkinitramfs
BuildRequires: digest(sha1:%{SOURCE0}) = 3760c0fc07077745abde140683e047d98ecaaaca
BuildRequires: digest(sha1:%{SOURCE1}) = 8b62981130de6fac98dcf0a947ced84bed5d438b

%description
The Linux Kernel

%package headers
Group: Development
Summary: Linux Userspace Headers
Requires: base-layout

%description headers
In order to compile anything, the Linux kernel needs to expose an
Application Programming Interface (API) for the system's C library
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
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make mrproper
make HOSTCC='gcc -D_GNU_SOURCE' headers_install
make HOSTCC='gcc -D_GNU_SOURCE' headers_check
make HOSTCC='gcc -D_GNU_SOURCE' INSTALL_HDR_PATH=dest headers_install
find dest -name .install -exec rm -v '{}' \;
find dest -name ..install.cmd -exec rm -v '{}' \;
cp %{SOURCE1} .config
sed -i 's@-LightCube@-%{release}@' .config
sed -i 's@HAVE_KERNEL_BZIP2@& if !XEN@' arch/x86/Kconfig
sed -i 's@HAVE_KERNEL_LZMA@& if !XEN@' arch/x86/Kconfig
sed -i 's@HAVE_KERNEL_XZ@& if !XEN@' arch/x86/Kconfig
sed -i 's@HAVE_KERNEL_LZO@& if !XEN@' arch/x86/Kconfig
make HOSTCFLAGS='-D_GNU_SOURCE' %{PMFLAGS}

%install
# Install the headers
mkdir -p %{buildroot}/include
cp -r dest/include/* %{buildroot}/include

# Install the modules
make INSTALL_MOD_PATH=%{buildroot} modules_install

# Install the kernel source
DIRNAME="/src/kernels/%{name}-%{version}-%{release}"
install -d "%{buildroot}$DIRNAME"
cp -a .config Module.symvers .version scripts include "%{buildroot}$DIRNAME"
install -d "%{buildroot}$DIRNAME/arch/x86/"
cp -a arch/x86/include "%{buildroot}$DIRNAME/arch/x86/"
find . -type f -a '(' -name Kconfig\* -o -name Makefile\* -o -name \*.s ')' | (
  while read file
  do
    install -d "%{buildroot}$DIRNAME/`dirname $file`"
    cp "$file" "%{buildroot}$DIRNAME/$file"
  done
)
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-%{release}/source"
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-%{release}/build"

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

%post
/bin/mkinitramfs %{version}-%{release}

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
/boot/System.map-%{version}-%{release}
/boot/config-%{version}-%{release}
/boot/vmlinux-%{version}-%{release}
/lib/firmware
%dir /lib/modules/%{version}-%{release}
/lib/modules/%{version}-%{release}/kernel
/lib/modules/%{version}-%{release}/modules.*

%files headers
%defattr(-,root,root)
/include/asm
/include/asm-generic
/include/drm
/include/linux
/include/mtd
/include/rdma
/include/scsi
/include/sound
/include/video
/include/xen

%files devel
%defattr(-,root,root)
/src/kernels/%{name}-%{version}-%{release}
/lib/modules/%{version}-%{release}/source
/lib/modules/%{version}-%{release}/build

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.3.2-1
- Initial version
