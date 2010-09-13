Summary: Logical Volume Manager 2
Name: LVM2
Version: 2.02.73
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://sourceware.org/lvm2
Source: http://dev.lightcube.us/sources/%{name}/%{name}.%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = 297feef08dced7d64bff9f5f8a47c1916fcb2afa
BuildRequires: readline-devel

%description
LVM2 refers to a new userspace toolset that provide logical volume management
facilities on linux. It is reasonably backwards-compatible with the original
LVM toolset.

%package libdevmapper-devel
Summary: Headers and libraries for developing with libdevmapper
Group: Development/Libraries
Requires: %{name}

%description libdevmapper-devel
Headers and libraries for developing with libdevmapper

%prep
%setup -q -n %{name}.%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
%ifarch x86_64
rm -rf %{buildroot}/usr/lib
ln -vs libdevmapper.so.1.02 %{buildroot}/usr/%{_lib}/libdevmapper.so
%endif

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%dir /etc/lvm
%config /etc/lvm/lvm.conf
/usr/%{_lib}/libdevmapper.so.1.02
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
/usr/share/man/man5/*
/usr/share/man/man8/*

%files libdevmapper-devel
%defattr (-,root,root)
/usr/include/libdevmapper.h
/usr/%{_lib}/libdevmapper.so

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.02.73-1
- Initial version
