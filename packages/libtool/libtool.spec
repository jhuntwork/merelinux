Summary: GNU Libtool
Name: libtool
Version: 2.4
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/libtool
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 149e9d7a993b643d13149a94d07bbca1085e601c

%description
%{name} is a generic library support script. It hides the complexity
of using shared libraries behind a consistent, portable interface.

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/libtool.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/libtool.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/libtool
/usr/bin/libtoolize
/usr/include/libltdl
/usr/include/ltdl.h
/usr/%{_lib}/libltdl.*
/usr/share/aclocal/argz.m4
/usr/share/aclocal/libtool.m4
/usr/share/aclocal/ltdl.m4
/usr/share/aclocal/ltoptions.m4
/usr/share/aclocal/ltsugar.m4
/usr/share/aclocal/ltversion.m4
/usr/share/aclocal/lt~obsolete.m4
/usr/share/info/libtool.info
/usr/share/info/libtool.info-1
/usr/share/info/libtool.info-2
/usr/share/libtool
/usr/share/man/man1/libtool.1.bz2
/usr/share/man/man1/libtoolize.1.bz2

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.4-1
- Upgrade to 2.4

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.10-1
- Upgrade to 2.2.10

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.6b-1
- Upgrade to 2.2.6b

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
