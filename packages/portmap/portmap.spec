Summary: portmap
Name: portmap
Version: 6.0
Release: 2
Group: System Environment/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://neil.brown.name/portmap
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tgz
Source1: http://dev.lightcube.us/svn/lightcubeos/!svn/bc/358/lightcube_os/trunk/packages/%{name}/%{name}.init

BuildRequires: digest(sha1:%{SOURCE0}) = 8133aaf1bdb0d0ba0b2d26e116e1e0397a3f027b
BuildRequires: digest(sha1:%{SOURCE1}) = f341e9225fe3f8ef87297d0f5ff13ba48e8a8f9c
BuildRequires: tcp_wrappers-devel

%description
Portmap is a server that converts RPC (Remote Procedure Call) program numbers
into DARPA protocol port numbers.

%prep
%setup -q -n %{name}_%{version}

%build
make

%install
install -dv %{buildroot}/usr/share/man/man8
install -dv %{buildroot}/{etc/init.d,sbin}
make BASEDIR=%{buildroot} install
install -vm0754 %{SOURCE1} %{buildroot}/etc/init.d/portmap
%{compress_man}

%clean
rm -rf %{buildroot}

%preun
/usr/sbin/remove_initd portmap || /bin/true

%files
%defattr(-,root,root)
/etc/init.d/portmap
/sbin/portmap
/sbin/pmap_dump
/sbin/pmap_set
/usr/share/man/man8/pmap_dump.8.bz2
/usr/share/man/man8/pmap_set.8.bz2
/usr/share/man/man8/portmap.8.bz2

%changelog
* Mon Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.0-2
- Add a bootscript for portmap

* Fri May 06 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.0-1
- Initial version
