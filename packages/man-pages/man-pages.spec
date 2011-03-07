Summary: Core System Man Pages
Name: man-pages
Version: 3.32
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.kernel.org/doc/man-pages
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = c4e7471cb6df211445ae5be9ced2b99ffa632327

%description
Provides core system man pages.

%package devel
Summary: System development man pages
Group: Development

%prep
%setup -q 

%install
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/share/man/man1/*
/usr/share/man/man2/*
/usr/share/man/man4/*
/usr/share/man/man5/*
/usr/share/man/man6/*
/usr/share/man/man7/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/usr/share/man/man3/*

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.32-1
- Upgrade to 3.32

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.25-1
- Upgrade to 3.25

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.24-1
- Upgrade to 3.24

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
