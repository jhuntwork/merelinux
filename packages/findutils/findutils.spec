Summary: GNU Findutils
Name: findutils
Version: 4.4.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/findutils
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc

%description
Utilities for searching files in a directory hierarchy.

%prep
%setup -q

%build
./configure --prefix=/usr --libexecdir=/usr/%{_lib}/findutils \
    --localstatedir=/var/lib/locate
make
make check

%install
make DESTDIR=%{buildroot} install
mkdir %{buildroot}/bin
mv -v %{buildroot}/usr/bin/find %{buildroot}/bin
sed -i 's/find:=${BINDIR}/find:=\/bin/' %{buildroot}/usr/bin/updatedb
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info %{_infodir}/find.info %{_infodir}/dir
/usr/bin/install-info %{_infodir}/find-maint.info %{_infodir}/dir

%preun
/usr/bin/install-info --delete %{_infodir}/find.info %{_infodir}/dir
/usr/bin/install-info --delete %{_infodir}/find-maint.info %{_infodir}/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/find
/usr/bin/locate
/usr/bin/oldfind
/usr/bin/updatedb
/usr/bin/xargs
/usr/%{_lib}/findutils
/usr/share/info/find-maint.info
/usr/share/info/find.info
/usr/share/man/man1/find.1
/usr/share/man/man1/locate.1
/usr/share/man/man1/updatedb.1
/usr/share/man/man1/xargs.1
/usr/share/man/man5/locatedb.5


%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
