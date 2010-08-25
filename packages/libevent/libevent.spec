Summary: libevent
Name: libevent
Version: 1.4.14b
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.libpng.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-stable.tar.gz

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = a00e037e4d3f9e4fe9893e8a2d27918c

%description
The libevent API provides a mechanism to execute a callback function when a
specific event occurs on a file descriptor or after a timeout has been reached.
Furthermore, libevent also support callbacks due to signals or regular
timeouts.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q -n %{name}-%{version}-stable

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/event_rpcgen.py
/usr/%{_lib}/libevent-1.4.so.2
/usr/%{_lib}/libevent-1.4.so.2.2.0
/usr/%{_lib}/libevent_core-1.4.so.2
/usr/%{_lib}/libevent_core-1.4.so.2.2.0
/usr/%{_lib}/libevent_extra-1.4.so.2
/usr/%{_lib}/libevent_extra-1.4.so.2.2.0

%files devel
%defattr(-,root,root)
/usr/include/evdns.h
/usr/include/event-config.h
/usr/include/event.h
/usr/include/evhttp.h
/usr/include/evrpc.h
/usr/include/evutil.h
/usr/%{_lib}/libevent.a
/usr/%{_lib}/libevent.la
/usr/%{_lib}/libevent.so
/usr/%{_lib}/libevent_core.a
/usr/%{_lib}/libevent_core.la
/usr/%{_lib}/libevent_core.so
/usr/%{_lib}/libevent_extra.a
/usr/%{_lib}/libevent_extra.la
/usr/%{_lib}/libevent_extra.so
/usr/share/man/man3/evdns.3
/usr/share/man/man3/event.3

%changelog
* Fri Aug 20 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.14b-1
- Initial version
