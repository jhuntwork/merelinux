Summary: mdadm
Name: mdadm
Version: 3.2.2
Release: 1
Group: Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://neil.brown.name/blog/mdadm
Source: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 8ec366a7e7f3ae3a8765d8f43f1d62234a80c698

%description
mdadm is a tool for managing Linux Software RAID arrays.

%prep
%setup -q

%build
make %{PMFLAGS} CC="gcc -Os -pipe"

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

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
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.2.2-1
- Initial version

* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.4-1
- Initial version
