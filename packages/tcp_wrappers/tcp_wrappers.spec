Summary: TCP Wrapper Programs
Name: tcp_wrappers
Version: 7.6
Release: 1
Group: System Environment/Utilities
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://ftp.porcupine.org/pub/security/index.html
Source0: http://dev.lightcube.us/sources/%{name}/%{name}_%{version}.tar.gz
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-shared_lib_plus_plus-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 61689ec85b80f4ca0560aef3473eccd9e9e80481
BuildRequires: digest(sha1:%{PATCH0}) = 915652d43c57f346d6f0a14eeaf706bbfed98ffa

%description
tcp_wrappers provides tiny daemon wrapper programs that can be installed
without any changes to existing software or to existing configuration
files.  The wrappers report the name of the client host and of the
requested service; the wrappers do not exchange information with the
client or server applications, and impose no overhead on the actual
conversation between the client and server applications.

%package devel
Summary: Headers and libraries for developing with libwrap
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with libwrap

%prep
%setup -q -n %{name}_%{version}
%patch0 -p1

%build
sed -i -e "s,^extern char \*malloc();,/* & */," scaffold.c
%ifarch x86_64
sed -i 's@/usr/lib@/usr/%{_lib}@g' Makefile
%endif
export LDFLAGS="%{LDFLAGS}"
make REAL_DAEMON_DIR=/usr/sbin STYLE=-DPROCESS_OPTIONS linux

%install
install -dv %{buildroot}/usr/{%{_lib},include,sbin,share/man/man{3,5,8}}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/man/man3/{hosts_ctl.3,request_init.3,request_set.3}
%{compress_man}
ln -sv hosts_access.3.bz2 %{buildroot}/usr/share/man/man3/hosts_ctl.3.bz2
ln -sv hosts_access.3.bz2 %{buildroot}/usr/share/man/man3/request_init.3.bz2
ln -sv hosts_access.3.bz2 %{buildroot}/usr/share/man/man3/request_set.3.bz2

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libwrap.so.0
/usr/%{_lib}/libwrap.so.0.7.6
/usr/sbin/safe_finger
/usr/sbin/tcpd
/usr/sbin/tcpdchk
/usr/sbin/tcpdmatch
/usr/sbin/try-from
/usr/share/man/man5/hosts_access.5.bz2
/usr/share/man/man5/hosts_options.5.bz2
/usr/share/man/man8/safe_finger.8.bz2
/usr/share/man/man8/tcpd.8.bz2
/usr/share/man/man8/tcpdchk.8.bz2
/usr/share/man/man8/tcpdmatch.8.bz2
/usr/share/man/man8/try-from.8.bz2

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libwrap.a
/usr/%{_lib}/libwrap.so
/usr/include/tcpd.h
/usr/share/man/man3/hosts_access.3.bz2
/usr/share/man/man3/hosts_ctl.3.bz2
/usr/share/man/man3/request_init.3.bz2
/usr/share/man/man3/request_set.3.bz2

%changelog
* Wed Oct 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.6-1
- Initial version
