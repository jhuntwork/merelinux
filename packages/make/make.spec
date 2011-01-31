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

BuildRequires: digest(sha1:%{SOURCE0}) = b8a8a99e4cb636a213aad3816dda827a92b9bbed

%description
Make is a tool which controls the generation of executables and other
non-source files of a program from the program's source files.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --infodir=/usr/share/info \
  --mandir=/usr/share/man
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/make.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/make.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/make
/usr/share/info/make.info
/usr/share/info/make.info-1
/usr/share/info/make.info-2
/usr/share/man/man1/make.1.bz2

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.82-1
- Upgrade to 3.82

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.81-1
- Initial version
