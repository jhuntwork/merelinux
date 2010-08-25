Summary: xfs File System Programs
Name: xfsprogs
Version: 3.1.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://xfs.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = 86d10178ee6897cb099c97303e6d9da0
BuildRequires: util-linux-ng-devel
BuildRequires: readline-devel

%description
%{name} provides core file system utilities associated with the
xfs filesystem

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --sbindir=/sbin \
  --libdir=/%{_lib} \
  --enable-readline
make

%install
make prefix=%{buildroot}/usr \
  PKG_SBIN_DIR=%{buildroot}/sbin \
  PKG_ROOT_SBIN_DIR=%{buildroot}/sbin \
  PKG_LIB_DIR=%{buildroot}/%{_lib} \
  PKG_ROOT_LIB_DIR=%{buildroot}/%{_lib} \
  install
make prefix=%{buildroot}/usr \
  PKG_SBIN_DIR=%{buildroot}/sbin \
  PKG_ROOT_SBIN_DIR=%{buildroot}/sbin \
  PKG_LIB_DIR=%{buildroot}/%{_lib} \
  PKG_ROOT_LIB_DIR=%{buildroot}/%{_lib} \
  install-dev
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/%{_lib}/libhandle.so.1
/%{_lib}/libhandle.so.1.0.3
/usr/share/doc/xfsprogs
/usr/share/man/man5/projects.5
/usr/share/man/man5/projid.5
/usr/share/man/man5/xfs.5
/usr/share/man/man8/fsck.xfs.8
/usr/share/man/man8/mkfs.xfs.8
/usr/share/man/man8/xfs_admin.8
/usr/share/man/man8/xfs_bmap.8
/usr/share/man/man8/xfs_check.8
/usr/share/man/man8/xfs_copy.8
/usr/share/man/man8/xfs_db.8
/usr/share/man/man8/xfs_estimate.8
/usr/share/man/man8/xfs_freeze.8
/usr/share/man/man8/xfs_fsr.8
/usr/share/man/man8/xfs_growfs.8
/usr/share/man/man8/xfs_info.8
/usr/share/man/man8/xfs_io.8
/usr/share/man/man8/xfs_logprint.8
/usr/share/man/man8/xfs_mdrestore.8
/usr/share/man/man8/xfs_metadump.8
/usr/share/man/man8/xfs_mkfile.8
/usr/share/man/man8/xfs_ncheck.8
/usr/share/man/man8/xfs_quota.8
/usr/share/man/man8/xfs_repair.8
/usr/share/man/man8/xfs_rtcp.8
/sbin/xfs_admin
/sbin/xfs_bmap
/sbin/xfs_check
/sbin/xfs_copy
/sbin/xfs_db
/sbin/xfs_estimate
/sbin/xfs_freeze
/sbin/xfs_fsr
/sbin/xfs_growfs
/sbin/xfs_info
/sbin/xfs_io
/sbin/xfs_logprint
/sbin/xfs_mdrestore
/sbin/xfs_metadump
/sbin/xfs_mkfile
/sbin/xfs_ncheck
/sbin/xfs_quota
/sbin/xfs_rtcp
/sbin/fsck.xfs
/sbin/mkfs.xfs
/sbin/xfs_repair

%files devel
%defattr(-,root,root)
/usr/include/xfs
/%{_lib}/libhandle.a
/%{_lib}/libhandle.la
/%{_lib}/libhandle.so
/usr/share/man/man3/*

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.2-1
- Initial version
