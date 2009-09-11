Summary: Gawk
Name: gawk
Version: 3.1.7
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gawk
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc

%description
Gawk is the GNU implementation of the awk command. The utility
interprets a special-purpose programming language that makes it
possible to handle many data-reformatting jobs with just a few
lines of code.

%prep
%setup -q

%build
./configure --prefix=/usr --libexecdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info %{_infodir}/gawk.info %{_infodir}/dir
/usr/bin/install-info %{_infodir}/gawkinet.info %{_infodir}/dir

%preun
/usr/bin/install-info --delete %{_infodir}/gawk.info %{_infodir}/dir
/usr/bin/install-info --delete %{_infodir}/gawkinet.info %{_infodir}/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/awk
/usr/bin/gawk
/usr/bin/gawk-%{version}
/usr/bin/igawk
/usr/bin/pgawk
/usr/bin/pgawk-%{version}
/usr/%{_lib}/awk
/usr/share/awk
/usr/share/info/gawk.info
/usr/share/info/gawkinet.info
/usr/share/man/man1/gawk.1
/usr/share/man/man1/igawk.1
/usr/share/man/man1/pgawk.1

%changelog
* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
