Summary: chkconfig
Name: chkconfig
Version: 1.3.30c
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.fastcoder.net/software/chkconfig
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, popt
BuildRequires: digest(%{SOURCE0}) = 592a1fe77f3844d7748adbab6357ee25
BuildRequires: popt-devel

%description
Chkconfig is a tool for managing the collection of symbolic links found in the
/etc/rc[0-6].d directories, on System V derived UNIX systems. It saves the
system administrator from the tedium of manually managing the scores of
symbolic links.

%prep
%setup -q

%build
./configure \
  --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/usr/share/locale/sr@Latn
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/sbin/chkconfig
/usr/sbin/alternatives
/usr/share/man/man8/alternatives.8
/usr/share/man/man8/chkconfig.8

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.30c-1
- Initial version
