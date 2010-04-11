Summary: GNU Libtool
Name: libtool
Version: 2.2.6b
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/libtool
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 07da460450490148c6d2df0f21481a25

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
find %{buildroot} -name "*.la" -exec rm -v '{}' \;

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

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.2.6b-1
- Upgrade to 2.2.6b

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
