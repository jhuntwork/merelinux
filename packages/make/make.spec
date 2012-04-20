Summary: GNU Make
Name: make
Version: 3.82
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/make
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: make-ar.h.patch

BuildRequires: digest(sha1:%{SOURCE0}) = b8a8a99e4cb636a213aad3816dda827a92b9bbed
BuildRequires: digest(sha1:%{PATCH0})  = a157c1727c0cd6b9ce4280453bc31a2314a07e04

%description
Make is a tool which controls the generation of executables and other
non-source files of a program from the program's source files.

%prep
%setup -q
%patch0 -p1
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
export LDFLAGS='--static'
./configure \
  --prefix='' \
  --infodir=/share/info \
  --mandir=/share/man
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/make
/share/man/man1/make.1.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.82-1
- Initial version
