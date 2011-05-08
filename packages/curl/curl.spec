Summary: cURL groks URLs
Name: curl
Version: 7.21.6
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://curl.haxx.se
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 049a3aff13d283f6e4ea1f9aa3aa6abc067fd42e
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
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{compress_man}

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
/usr/share/man/man3/*


%changelog
* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.6-1
- Upgrade to 7.21.6

* Thu Aug 19 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.21.1-1
- Initial version
