Summary: The Linux Kernel for Xen dom0 hosts
Name: linux-xen
Version: 2.6.32.13
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://dev.lightcube.us/sources/linux/%{name}-%{version}.tar.bz2

Requires: base-layout
BuildRequires: digest(sha1:%{SOURCE0}) = 2b88b3f3b9b28c078d4ed37b2cb47826e193f534

%ifarch x86_64
Source1: http://dev.lightcube.us/sources/linux-configs/%{name}-config-%{version}-x86_64
BuildRequires: digest(sha1:%{SOURCE1}) = 4cf77258c4e1583ba456558ced2c649f7c8989ca
%endif

%description
The Linux Kernel for Xen dom0 hosts

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
cp %{SOURCE1} .config
make

%install
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
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-xen/source"
ln -nsf "$DIRNAME" "%{buildroot}/lib/modules/%{version}-xen/build"

# Install the kernel image, system.map and config
mkdir %{buildroot}/boot
cp System.map %{buildroot}/boot/System.map-xen-%{version}-%{release}
cp .config %{buildroot}/boot/config-xen-%{version}-%{release}
%ifarch x86_64
cp arch/x86_64/boot/vmlinuz %{buildroot}/boot/vmlinux-xen-%{version}-%{release}
%endif

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,root)
/boot/System.map-xen-%{version}-%{release}
/boot/config-xen-%{version}-%{release}
/boot/vmlinux-xen-%{version}-%{release}
/lib/firmware
%dir /lib/modules/%{version}-xen
/lib/modules/%{version}-xen/kernel
/lib/modules/%{version}-xen/modules.*

%files devel
%defattr(-,root,root)
/usr/src/kernels/%{name}-%{version}-%{release}
/lib/modules/%{version}-xen/source
/lib/modules/%{version}-xen/build

%changelog
* Wed Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.32.13-1
- Initial version
