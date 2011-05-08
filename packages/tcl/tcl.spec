Summary: Tool Command Language
Name: tcl
Version: 8.5.9
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.tcl.tk
Source0: http://dev.lightcube.us/sources/%{name}/%{name}%{version}-src.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ae87c5e58ba20760d9bc77117d219bbf1b6a5557

%description
Tcl (Tool Command Language) is a very powerful but easy to learn dynamic
programming language, suitable for a very wide range of uses, including web and
desktop applications, networking, administration, testing and many more. Open
source and business-friendly, Tcl is a mature yet evolving language that is
truly cross platform, easily deployed and highly extensible.

%package devel
Summary: Headers and Libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Headers and Libraries for developing with %{name}

%prep
%setup -q -n %{name}%{version}

%build
export LDFLAGS="%{LDFLAGS}"
cd unix
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make %{PMFLAGS}
TZ=UTC make test

%install
cd unix
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/tclsh8.5
/usr/lib/tcl8.5
/usr/lib/tcl8
/usr/%{_lib}/libtcl8.5.so
/usr/share/man/man1/tclsh.1.bz2
/usr/share/man/mann/*

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libtclstub8.5.a
/usr/%{_lib}/tclConfig.sh
/usr/include/*
/usr/share/man/man3/*

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.5.9-1
- Initial version
