Summary: psmisc
Name: psmisc
Version: 22.10
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://psmisc.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = e881383e7f399121cd0ce744f97d91a5

%description
The PSmisc package is a set of some small useful utilities that use the proc filesystem.

%prep
%setup -q

%build
./configure --prefix=/usr --exec-prefix=""
make

%install
make DESTDIR=%{buildroot} install
mkdir -pv %{buildroot}/usr/bin
mv -v %{buildroot}/bin/pstree* %{buildroot}/usr/bin
ln -sv killall %{buildroot}/bin/pidof
rm -vf %{buildroot}/usr/bin/pstree.x11
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/fuser
/bin/killall
/bin/pidof
/bin/prtstat
/usr/bin/pstree
/usr/share/man/man1/fuser.1
/usr/share/man/man1/killall.1
/usr/share/man/man1/peekfd.1
/usr/share/man/man1/prtstat.1
/usr/share/man/man1/pstree.1

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 22.10-1
- Upgrade to 22.10

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
