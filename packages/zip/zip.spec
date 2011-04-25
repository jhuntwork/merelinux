Summary: Zip archive utility
Name: zip
Version: 3.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://infozip.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}30.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = c9f4099ecf2772b53c2dd4a8e508064ce015d182

%description
Zip is a compression and file packaging/archive utility.

%prep
%setup -q -n zip30

%build
export LDFLAGS=%{LDFLAGS}
make -f unix/Makefile generic_gcc

%install
make prefix=%{buildroot}/usr MANDIR=%{buildroot}/usr/share/man -f unix/Makefile install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/zip
/usr/bin/zipcloak
/usr/bin/zipnote
/usr/bin/zipsplit
/usr/share/man/zip.1.bz2
/usr/share/man/zipcloak.1.bz2
/usr/share/man/zipnote.1.bz2
/usr/share/man/zipsplit.1.bz2

%changelog
* Mon Apr 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0-1
- Initial version
