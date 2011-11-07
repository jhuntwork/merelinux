Summary: GNU Parted
Name: parted
Version: 3.0
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/parted
Source0: http://ftp.gnu.org/gnu/parted/parted-3.0.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 6e8f7a2b042ba6222e8ea245a05136669fccec7f
BuildRequires: util-linux-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: LVM2-libdevmapper-devel

%description
GNU Parted manipulates partition tables. This is useful for creating
space for new operating systems, reorganizing disk usage, copying data on
hard disks and disk imaging. The package contains a library, libparted,
as well as well as a command-line frontend, parted, which can also be used in
scripts.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/parted.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/parted.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/%{_lib}/libparted.so.1
/usr/%{_lib}/libparted.so.1.0.0
/usr/sbin/parted
/usr/sbin/partprobe
/usr/share/info/parted.info
/usr/share/man/man8/parted.8.bz2
/usr/share/man/man8/partprobe.8.bz2

%files devel
%defattr(-,root,root)
/usr/include/parted
/usr/%{_lib}/libparted.a
/usr/%{_lib}/libparted.la
/usr/%{_lib}/libparted.so
/usr/%{_lib}/pkgconfig/libparted.pc

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0-2
- Build in libdevmapper support
- Optimize for size

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0-1
- Upgrade to 3.0

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.3-1
- Initial version
