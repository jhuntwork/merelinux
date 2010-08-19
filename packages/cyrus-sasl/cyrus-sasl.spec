Summary: The Simple Authentication and Security Layer
Name: cyrus-sasl
Version: 2.1.23
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://asg.web.cmu.edu/sasl
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-gcc44-1.patch

Requires: base-layout, glibc, openssl, Linux-PAM, gdbm, db
BuildRequires: digest(%{SOURCE0}) = 2eb0e48106f0e9cd8001e654f267ecbc
BuildRequires: digest(%{PATCH0}) = 04f9bf36c4a1f994875bca5c0f1e020c
BuildRequires: openssl-devel, Linux-PAM-devel, gdbm-devel, db-devel

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

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --with-dbpath=/var/lib/sasl/sasldb2 \
  --with-saslauthd=/var/run/saslauthd \
  --mandir=/usr/share/man \
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
%dir /usr/lib/sasl2
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
/usr/share/man/man8/pluginviewer.8
/usr/share/man/man8/saslauthd.8
/usr/share/man/man8/sasldblistusers2.8
/usr/share/man/man8/saslpasswd2.8

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
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.1.23-1
- Initial version
