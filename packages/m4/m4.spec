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

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/m4.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/m4.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/m4
/usr/share/info/m4.info
/usr/share/info/m4.info-1
/usr/share/info/m4.info-2
/usr/share/man/man1/m4.1.bz2

%changelog
* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.16-1
- Upgrade to 1.4.16

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.15-1
- Upgrade to 1.4.15

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.14-1
- Upgrade to 1.4.14

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
