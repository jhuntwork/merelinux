Summary: expect
Name: expect
Version: 5.45
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://expect.sourceforge.net
Source0: http://dev.lightcube.us/sources/%{name}/%{name}%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = e634992cab35b7c6931e1f21fbb8f74d464bd496
BuildRequires: tcl-devel

%description
Expect is a tool for automating interactive applications such as telnet, ftp,
passwd, fsck, rlogin, tip, etc.

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
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --mandir=/usr/share/man
make %{PMFLAGS}
make test

%install
make DESTDIR=%{buildroot} install
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/expect
/usr/bin/autoexpect
/usr/bin/autopasswd
/usr/bin/cryptdir
/usr/bin/decryptdir
/usr/bin/dislocate
/usr/bin/ftp-rfc
/usr/bin/kibitz
/usr/bin/lpunlock
/usr/bin/mkpasswd
/usr/bin/multixterm
/usr/bin/passmass
/usr/bin/rftp
/usr/bin/rlogin-cwd
/usr/bin/timed-read
/usr/bin/timed-run
/usr/bin/tknewsbiff
/usr/bin/tkpasswd
/usr/bin/unbuffer
/usr/bin/weather
/usr/bin/xkibitz
/usr/bin/xpstat
/usr/%{_lib}/expect5.45
/usr/share/man/man1/*

%files devel
%defattr(-,root,root)
/usr/include/*
/usr/share/man/man3/libexpect.3.bz2

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.45-1
- Initial version
