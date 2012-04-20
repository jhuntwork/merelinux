Summary: cURL groks URLs
Name: curl
Version: 7.22.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://curl.haxx.se
Source0: http://curl.haxx.se/download/curl-7.22.0.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 8e7b2b0ca933812614ec0eade2f83e77632247d6
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
curl is a command line tool for transferring data with URL syntax, supporting
FTP, FTPS, HTTP, HTTPS, SCP, SFTP, TFTP, TELNET, DICT, LDAP, LDAPS, FILE,
IMAP, SMTP, POP3, RTMP and RTSP. curl supports SSL certificates, HTTP POST,
HTTP PUT, FTP uploading, HTTP form based upload, proxies, cookies,
user+password authentication (Basic, Digest, NTLM, Negotiate, kerberos...),
file transfer resume, proxy tunneling and a busload of other useful tricks.

%package devel
Summary: Libraries and headers for developing with libmagic
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and headers for developing with curl.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-ca-bundle=/etc/ssl/ca-bundle.crt
make

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/curl
/usr/share/man/man1/curl.1.bz2
/usr/%{_lib}/libcurl.so.4
/usr/%{_lib}/libcurl.so.4.2.0

%files devel
%defattr(-,root,root)
/usr/bin/curl-config
/usr/include/curl
/usr/%{_lib}/libcurl.a
/usr/%{_lib}/libcurl.la
/usr/%{_lib}/libcurl.so
/usr/%{_lib}/pkgconfig/libcurl.pc
/usr/share/man/man1/curl-config.1.bz2
/usr/share/man/man3/*.bz2

%changelog
* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.22.0-1
- Upgrade to 7.22.0
- Fix (again) the ca-bundle - use the one provided by OpenSSL
- Optimize for size

* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.7-2
- Fix included certificate bundle

* Sun Aug 20 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.7-1
- Upgrade to 7.21.7
- Add a full CA bundle

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.6-1
- Upgrade to 7.21.6

* Thu Aug 19 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.1-1
- Initial version
