Summary: GNU Patch
Name: patch
Version: 2.6.1
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.gnu.org/projects/patch
Source0: ftp://ftp.gnu.org/gnu/patch/patch-2.6.1.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = 8cc3485aa433b8feb70f6783efb766554230fee8
BuildRequires: ed 

%description
Patch allows merging of textual changes

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr
make %{PMFLAGS}
make check

%install
make prefix=%{buildroot}/usr mandir=%{buildroot}/usr/share/man install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/patch
/usr/share/man/man1/patch.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-3
- Optimize for size
- Remove testsuite patch since ed is available

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-2
- Add in a patch for the testsuite

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-1
- Upgrade to 2.6.1

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
