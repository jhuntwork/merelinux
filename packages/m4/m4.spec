Summary: GNU M4
Name: m4
Version: 1.4.16
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/m4
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 0390c77780ab4cd65b07fe4e2d23e4e39769f967

%description
M4 is a macro processor. It copies its input to the output,
expanding macros as it goes.

%prep
%setup -q
%{config_musl}
sed -i '/abort/d' lib/freadahead.c

%build
export CFLAGS="-D_GNU_SOURCE -DSLOW_BUT_NO_HACKS -Os"
./configure \
  --prefix=''
make %{PMFLAGS}
#make check

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
rm -rf %{buildroot}/lib
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/m4
/share/man/man1/m4.1.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.16-1
- Initial version
