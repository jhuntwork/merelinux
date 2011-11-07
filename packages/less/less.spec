Summary: less
Name: less
Version: 443
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/less
Source0: ftp://ftp.gnu.org/gnu/less/less-443.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 72cf3d3c77990e04ad04ea63b377b893c8a7a2cd
BuildRequires: ncurses-devel

%description
Less allows forward and backwards page viewing through the contents of a file

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --sysconfdir=/etc
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/less
/usr/bin/lessecho
/usr/bin/lesskey
/usr/share/man/man1/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 443-2
- Optimize for size

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 443-1
- Upgrade to 443

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 436-1
- Upgrade to 436

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
