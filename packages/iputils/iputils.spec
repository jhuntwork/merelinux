Summary: iputils
Name: iputils
Version: 20101006
Release: 1
Group: System Environment/Base
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.skbuff.net/iputils
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-s%{version}.tar.bz2
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-s%{version}-debian_fixes-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = a08cc5423a7bf940205f2353fe3d129cd39ff242
BuildRequires: digest(sha1:%{PATCH0})  = d236f4acacb71b038d37447a69cd03fd0dee5060
BuildRequires: openssl-devel

%description
The iputils package is set of small useful utilities for Linux networking, such as
ping, clockdiff and tracepath

%prep
%setup -q -n %{name}-s%{version}
%patch0 -p1

%build
make

%install
install -dv %{buildroot}/{,s}bin
install -dv %{buildroot}/usr/sbin
install ping{,6} %{buildroot}/bin/
install tracepath{,6} %{buildroot}/bin/
install rdisc %{buildroot}/sbin/
install clockdiff %{buildroot}/usr/sbin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/ping
/bin/ping6
/bin/tracepath
/bin/tracepath6
/sbin/rdisc
/usr/sbin/clockdiff

%changelog
* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20101006-1
- Initial version
