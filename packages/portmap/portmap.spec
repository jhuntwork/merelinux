Summary: portmap
Name: portmap
Version: 6.0
Release: 1
Group: System Environment/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://neil.brown.name/portmap
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tgz

BuildRequires: digest(sha1:%{SOURCE0}) = 8133aaf1bdb0d0ba0b2d26e116e1e0397a3f027b
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
install -dv %{buildroot}/sbin
make BASEDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

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
* Fri May 06 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.0-1
- Initial version
