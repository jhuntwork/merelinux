Summary: Logical Volume Manager 2
Name: LVM2
Version: 2.02.88
Release: 1
Group: Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sourceware.org/lvm2
Source0: ftp://sources.redhat.com/pub/lvm2/LVM2.2.02.88.tgz

Requires: %{name}-libdevmapper >= %{version}
BuildRequires: digest(sha1:%{SOURCE0}) = 05a4fb09cb5e3d680ad1b268c941968853fb1979
BuildRequires: readline-devel

%description
LVM2 refers to a new userspace toolset that provide logical volume management
facilities on linux. It is reasonably backwards-compatible with the original
LVM toolset.

%package libdevmapper
Summary: Library for using LVM2-libdevmapper functions
Group: System/Libraries

%description libdevmapper
Libraries for using LVM2-libdevmapper functions

%package libdevmapper-devel
Summary: Headers and libraries for developing with libdevmapper
Group: Development/Libraries
Requires: %{name}-libdevmapper >= %{version}

%description libdevmapper-devel
Headers and libraries for developing with libdevmapper

%prep
%setup -q -n %{name}.%{version}

%build
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}
%ifarch x86_64
rm -rf %{buildroot}/usr/lib
ln -vs libdevmapper.so.1.02 %{buildroot}/usr/%{_lib}/libdevmapper.so
%endif

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /etc/lvm
%config /etc/lvm/lvm.conf
/usr/sbin/dmsetup
/usr/sbin/fsadm
/usr/sbin/lvchange
/usr/sbin/lvconvert
/usr/sbin/lvcreate
/usr/sbin/lvdisplay
/usr/sbin/lvextend
/usr/sbin/lvm
/usr/sbin/lvmchange
/usr/sbin/lvmconf
/usr/sbin/lvmdiskscan
/usr/sbin/lvmdump
/usr/sbin/lvmsadc
/usr/sbin/lvmsar
/usr/sbin/lvreduce
/usr/sbin/lvremove
/usr/sbin/lvrename
/usr/sbin/lvresize
/usr/sbin/lvs
/usr/sbin/lvscan
/usr/sbin/pvchange
/usr/sbin/pvck
/usr/sbin/pvcreate
/usr/sbin/pvdisplay
/usr/sbin/pvmove
/usr/sbin/pvremove
/usr/sbin/pvresize
/usr/sbin/pvs
/usr/sbin/pvscan
/usr/sbin/vgcfgbackup
/usr/sbin/vgcfgrestore
/usr/sbin/vgchange
/usr/sbin/vgck
/usr/sbin/vgconvert
/usr/sbin/vgcreate
/usr/sbin/vgdisplay
/usr/sbin/vgexport
/usr/sbin/vgextend
/usr/sbin/vgimport
/usr/sbin/vgimportclone
/usr/sbin/vgmerge
/usr/sbin/vgmknodes
/usr/sbin/vgreduce
/usr/sbin/vgremove
/usr/sbin/vgrename
/usr/sbin/vgs
/usr/sbin/vgscan
/usr/sbin/vgsplit
/usr/share/man/man5/*.bz2
/usr/share/man/man8/*.bz2

%files libdevmapper
%defattr (-,root,root)
/usr/%{_lib}/libdevmapper.so.1.02

%files libdevmapper-devel
%defattr (-,root,root)
/usr/include/libdevmapper.h
/usr/%{_lib}/libdevmapper.so

%changelog
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.02.88-1
- Upgrade to 2.02.88
- Optimize for size
- Package runtime library separately

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.02.73-1
- Initial version
