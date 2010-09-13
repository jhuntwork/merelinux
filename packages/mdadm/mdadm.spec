Summary: mdadm
Name: mdadm
Version: 3.1.4
Release: 1
Group: Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://neil.brown.name/blog/mdadm
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 4ee43922d38b15a930daaaa026ef1b4efacdbc8a

%description
mdadm is a tool for managing Linux Software RAID arrays.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/lib/udev/rules.d/64-md-raid.rules
/sbin/mdadm
/sbin/mdmon
/usr/share/man/man4/md.4.bz2
/usr/share/man/man5/mdadm.conf.5.bz2
/usr/share/man/man8/mdadm.8.bz2
/usr/share/man/man8/mdmon.8.bz2

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.4-1
- Initial version
