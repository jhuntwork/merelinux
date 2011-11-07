Summary: iputils
Name: iputils
Version: 20101006
Release: 2
Group: System Environment/Base
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.skbuff.net/iputils
Source0: http://www.skbuff.net/iputils/iputils-s20101006.tar.bz2
Patch0:  https://raw.github.com/jhuntwork/LightCube-OS/master/packages/iputils/debian-fixes.patch

BuildRequires: digest(sha1:%{SOURCE0}) = a08cc5423a7bf940205f2353fe3d129cd39ff242
BuildRequires: digest(sha1:%{PATCH0})  = d236f4acacb71b038d37447a69cd03fd0dee5060
BuildRequires: openssl-devel

%description
The iputils package is set of small useful utilities for Linux networking, such as
ping, clockdiff and tracepath

%prep
%setup -q -n %{name}-s%{version}
%patch0 -p1
sed -i 's@-O2@-Os -pipe@' Makefile

%build
make %{PMFLAGS}

%install
install -dv %{buildroot}/{,s}bin
install -dv %{buildroot}/usr/sbin
install ping{,6} %{buildroot}/bin/
install tracepath{,6} %{buildroot}/bin/
install rdisc %{buildroot}/sbin/
install clockdiff %{buildroot}/usr/sbin/
%{strip}

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
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20101006-2
- Optimize for size

* Tue Aug 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20101006-1
- Initial version
