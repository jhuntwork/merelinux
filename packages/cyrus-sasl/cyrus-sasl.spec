Summary: The Simple Authentication and Security Layer
Name: cyrus-sasl
Version: 2.1.23
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://asg.web.cmu.edu/sasl
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-gcc44-1.patch
Patch1: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-db-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 5df33a6788d6cd8329b109eff777c6cfae1a21bd
BuildRequires: digest(sha1:%{PATCH0}) = 0343b15c40d4a62643f21dc541fffa12d1efa347
BuildRequires: digest(sha1:%{PATCH1}) = 828fe0212f72d7fd1294fffa04698de7412ac2cd
BuildRequires: openssl-devel
BuildRequires: Linux-PAM-devel
BuildRequires: gdbm-devel
BuildRequires: db-devel

%description
SASL is the Simple Authentication and Security Layer, a method for adding
authentication support to connection-based protocols

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --sysconfdir=/etc/sasl2 \
  --with-dbpath=/var/lib/sasl/sasldb2 \
  --with-saslauthd=/var/run/saslauthd \
  --mandir=/usr/share/man \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/sasl2
%{compress_man}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
%dir /usr/lib/sasl2
%dir /etc/sasl2
/usr/lib/sasl2/libanonymous.so.2
/usr/lib/sasl2/libanonymous.so.2.0.23
/usr/lib/sasl2/libcrammd5.so.2
/usr/lib/sasl2/libcrammd5.so.2.0.23
/usr/lib/sasl2/libdigestmd5.so.2
/usr/lib/sasl2/libdigestmd5.so.2.0.23
/usr/lib/sasl2/libotp.so.2
/usr/lib/sasl2/libotp.so.2.0.23
/usr/lib/sasl2/libplain.so.2
/usr/lib/sasl2/libplain.so.2.0.23
/usr/lib/sasl2/libsasldb.so.2
/usr/lib/sasl2/libsasldb.so.2.0.23
/usr/%{_lib}/libsasl2.so.2
/usr/%{_lib}/libsasl2.so.2.0.23
/usr/sbin/pluginviewer
/usr/sbin/saslauthd
/usr/sbin/sasldblistusers2
/usr/sbin/saslpasswd2
/usr/sbin/testsaslauthd
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/usr/lib/sasl2/libanonymous.la
/usr/lib/sasl2/libanonymous.so
/usr/lib/sasl2/libcrammd5.la
/usr/lib/sasl2/libcrammd5.so
/usr/lib/sasl2/libdigestmd5.la
/usr/lib/sasl2/libdigestmd5.so
/usr/lib/sasl2/libotp.la
/usr/lib/sasl2/libotp.so
/usr/lib/sasl2/libplain.la
/usr/lib/sasl2/libplain.so
/usr/lib/sasl2/libsasldb.la
/usr/lib/sasl2/libsasldb.so
/usr/%{_lib}/libsasl2.la
/usr/%{_lib}/libsasl2.so
/usr/share/man/man3/sasl*
/usr/include/sasl

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.1.23-2
- Rebuild against db-5.1.19

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.1.23-1
- Initial version
