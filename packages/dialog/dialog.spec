%define release_vrs 1.1
%define release_date    20110302
Summary: dialog
Name: dialog
Version: %{release_vrs}.%{release_date}
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: Critical OS
Vendor: Critical Mention
URL: http://invisible-island.net/dialog
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{release_vrs}-%{release_date}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = ba4e79abaf579e0d23f247ae65196437f8d8e031
BuildRequires: ncurses-devel

%description
Udev provides a dynamic /dev directory, and hooks userspace into kernel device events.

%prep
%setup -q -n %{name}-%{release_vrs}-%{release_date}

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make

%install
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/dialog
/usr/share/man/man1/dialog.1.bz2

%changelog
* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.20110302-1
- Initial version
