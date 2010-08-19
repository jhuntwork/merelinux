Summary: GNU Parted
Name: parted
Version: 2.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/parted
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, util-linux-ng, readline, ncurses
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 30ceb6df7e8681891e865e2fe5a7903d
BuildRequires: util-linux-ng-devel, readline-devel, ncurses-devel

%description
GNU Parted manipulates partition tables. This is useful for creating
space for new operating systems, reorganizing disk usage, copying data on
hard disks and disk imaging. The package contains a library, libparted,
as well as well as a command-line frontend, parted, which can also be used in
scripts.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --disable-device-mapper
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/parted.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/parted.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/%{_lib}/libparted.so.0
/usr/%{_lib}/libparted.so.0.0.1
/usr/sbin/parted
/usr/sbin/partprobe
/usr/share/info/parted.info
/usr/share/man/man8/parted.8
/usr/share/man/man8/partprobe.8

%files devel
%defattr(-,root,root)
/usr/include/parted
/usr/%{_lib}/libparted.a
/usr/%{_lib}/libparted.la
/usr/%{_lib}/libparted.so
/usr/%{_lib}/pkgconfig/libparted.pc

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.3-1
- Initial version
