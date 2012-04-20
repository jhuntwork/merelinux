Summary: GNU Streams Editor
Name: sed
Version: 4.2.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/sed
Source0: http://ftp.gnu.org/gnu/sed/sed-4.2.1.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = ace93d23eabc00d3a8187ecf07d3a02b1b297810

%description
Sed is used to filter text and perform modifications on it.

%prep
%setup -q
%{config_musl}

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
export LDFLAGS='--static'
./configure \
  --prefix=''
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
rm -f %{buildroot}/lib/charset.alias
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/sed
/share/man/man1/sed.1.bz2

%changelog
* Thu Apr 19 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-1
- Initial version
