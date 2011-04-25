Summary: UnZip .zip archive extracter
Name: unzip
Version: 6.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://infozip.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}60.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = abf7de8a4018a983590ed6f5cbd990d4740f8a22

%description
Utility for extracting and viewing files in .zip archives.

%prep
%setup -q -n unzip60

%build
make -f unix/Makefile linux_noasm

%install
make prefix=%{buildroot}/usr MANDIR=%{buildroot}/usr/share/man install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/unzip
/usr/bin/funzip
/usr/bin/unzipsfx
/usr/bin/zipgrep
/usr/bin/zipinfo
/usr/share/man/funzip.1.bz2
/usr/share/man/unzip.1.bz2
/usr/share/man/unzipsfx.1.bz2
/usr/share/man/zipgrep.1.bz2
/usr/share/man/zipinfo.1.bz2

%changelog
* Sat Apr 23 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 6.0-1
- Initial version
