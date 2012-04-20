Summary: The Expat XML Parser
Name: expat
Version: 2.0.1
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://expat.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 663548c37b996082db1f2f2c32af060d7aa15c2d

%description
Expat is an XML parser library written in C. It is a
stream-oriented parser in which an application registers handlers
for things the parser might find in the XML document (like start tags).

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q
%{config_musl}

%build
export CFLAGS="-D_GNU_SOURCE -Os"
export LDFLAGS="--static"
./configure \
  --prefix='' \
  --disable-shared \
  --mandir=/share/man
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/xmlwf
/share/man/man1/xmlwf.1.bz2

%files devel
%defattr(-,root,root)
/include/expat.h
/include/expat_external.h
/lib/libexpat.a
/lib/libexpat.la

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.1-1
- Initial version
