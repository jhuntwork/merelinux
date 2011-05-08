Summary: DejaGnu
Name: dejagnu
Version: 1.5
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/dejagnu
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

Requires: tcl
Requires: expect
BuildRequires: digest(sha1:%{SOURCE0}) = bd84c71e0587af0278a9b6a404d6da1b92df66cd
BuildRequires: gcc-c++

%description
DejaGnu is a framework for testing other programs. Its purpose is to provide a
single front end for all tests. Think of it as a custom library of Tcl
procedures crafted to support writing a test harness. A test harness is the
testing infrastructure that is created to support a specific program or tool.
Each program can have multiple testsuites, all supported by a single test
harness. DejaGnu is written in Expect, which in turn uses Tcl -- Tool command
language.

%package devel
Summary: Header for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Header for developing with %{name}

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}

%post
/usr/bin/install-info /usr/share/info/dejagnu.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/dejagnu.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/runtest
/usr/share/dejagnu
/usr/share/info/dejagnu.info
/usr/share/man/man1/runtest.1.bz2

%files devel
%defattr(-,root,root)
/usr/include/dejagnu.h

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5-1
- Initial version
