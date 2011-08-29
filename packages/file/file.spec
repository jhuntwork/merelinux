Summary: Fine Free File Command
Name: file
Version: 5.06
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://darwinsys.com/file
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ad7cd2334a4e386c7647c69fba3cc8ec6b76c6ca
BuildRequires: zlib-devel

%description
The file command is "a file type guesser", that is, a command-line tool that
tells you in words what kind of data a file contains. It does not rely on
filename extensions, but looks at the contents of a file to determine its type.

%package devel
Summary: Libraries and headers for developing with libmagic
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with libmagic

%prep
%setup -q
# Move the datadir location from /usr/share/misc to /usr/share/file
sed -i 's/misc/file/' configure

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/file
/usr/%{_lib}/libmagic.so.1
/usr/%{_lib}/libmagic.so.1.0.0
/usr/share/man/man1/file.1.bz2
/usr/share/man/man4/magic.4.bz2
/usr/share/file

%files devel
%defattr(-,root,root)
/usr/include/magic.h
/usr/%{_lib}/libmagic.a
/usr/%{_lib}/libmagic.la
/usr/%{_lib}/libmagic.so
/usr/share/man/man3/libmagic.3.bz2

%changelog
* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.06-1
- Upgrade to 5.06

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.05-1
- Upgrade to 5.05

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.04-2
- Make datadir /usr/share/file instead of /usr/share/misc

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.04-1
- Upgrade to 5.04

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
