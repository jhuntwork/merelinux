Summary: GNU Patch
Name: patch
Version: 2.6.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.gnu.org/projects/patch
Source0: http://ftp.gnu.org/gnu/patch/patch-2.6.1.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = 8cc3485aa433b8feb70f6783efb766554230fee8

%description
Patch allows merging of textual changes

%prep
%setup -q
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os'
./configure \
  --prefix=''
make %{PMFLAGS}
#make check

%install
make prefix=%{buildroot} mandir=%{buildroot}/share/man install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/patch
/share/man/man1/patch.1.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-1
- Initial version
