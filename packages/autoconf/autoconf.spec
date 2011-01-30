Summary: GNU Autoconf
Name: autoconf
Version: 2.68
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.gnu.org/software/autoconf
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = b534c293b22048c022b1ff3a372b9c03f26170b4

%description
Autoconf is an extensible package of M4 macros that produce
shell scripts to automatically configure software source code packages.

%prep
%setup -q

%build
./configure --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/autoconf.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/standards.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/autoconf.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/standards.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/autoconf
/usr/bin/autoheader
/usr/bin/autom4te
/usr/bin/autoreconf
/usr/bin/autoscan
/usr/bin/autoupdate
/usr/bin/ifnames
/usr/share/autoconf
/usr/share/info/autoconf.info
/usr/share/info/standards.info
/usr/share/man/man1/*

%changelog
* Fri Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.68-1
- Upgrade to 2.68

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.66-1
- Upgrade to 2.66

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.65-1
- Initial version
