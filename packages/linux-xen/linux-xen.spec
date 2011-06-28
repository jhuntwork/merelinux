Summary: The Linux Kernel for Xen dom0 hosts
Name: linux-xen
Version: 2.6.32.41
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org
Source0: http://dev.lightcube.us/sources/linux-xen/%{name}-%{version}.tar.bz2
Patch0:  http://dev.lightcube.us/svn/lightcubeos/!svn/bc/389/lightcube_os/trunk/packages/%{name}/%{name}-3ware_sas-1.patch

Requires: base-layout
BuildRequires: digest(sha1:%{SOURCE0}) = 0ab6af3bfd68572a9c6623b1c23502acf4aa8a83
BuildRequires: digest(sha1:%{PATCH0})  = dc5c4a8874bd986d85433a8c602fee27c0df1f31

%ifarch x86_64
Source1:  http://dev.lightcube.us/svn/lightcubeos/!svn/bc/389/lightcube_os/trunk/packages/%{name}/%{name}-config.x86_64
BuildRequires: digest(sha1:%{SOURCE1}) = 767c979e4b889a0a1454c3e6d7cc10538fc32bb5
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
%patch0 -p1

%build
make mrproper
cp %{SOURCE1} .config
make %{PMFLAGS}

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
cp arch/x86_64/boot/bzImage %{buildroot}/boot/vmlinux-xen-%{version}-%{release}
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
* Fri Jun 24 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.32.41-1
- Upgrade to 2.6.32.41
- Add support for 3ware SAS card

* Fri Dec 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.32.26-1
- Upgrade to 2.6.32.26

* Wed Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.32.13-1
- Initial version
