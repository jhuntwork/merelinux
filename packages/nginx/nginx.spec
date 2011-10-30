Summary: nginx HTTP Server
Name: nginx
Version: 1.0.8
Release: 1
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://nginx.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/sources/%{name}/%{name}.init

BuildRequires: digest(sha1:%{SOURCE0}) = d0ab9329e6aa774f655bfa5ac0b30c840f1acd88
BuildRequires: digest(sha1:%{SOURCE1}) = e454f6a53e5a736a8478a8df49345f7b04e6dc8c
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
nginx [engine x] is a HTTP and reverse proxy server, as well as a mail proxy
server

%prep
%setup -q

%build
export CFLAGS="-Os -pipe -Wall"
./configure \
  --prefix=/srv/nginx \
  --user=nginx \
  --group=nginx \
  --sbin-path=/usr/sbin/nginx \
  --conf-path=/etc/nginx/nginx.conf \
  --pid-path=/var/run/nginx.pid \
  --lock-path=/var/lock/nginx.lock \
  --error-log-path=/var/log/nginx-error.log \
  --http-log-path=/var/log/nginx-access.log \
  --with-http_ssl_module \
  --with-debug
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
sed -i 's@SCRIPT_FILENAME.*/script@SCRIPT_FILENAME $document_root$fastcgi_script_name;@' \
  %{buildroot}/etc/nginx/nginx.conf
install -m0754 %{SOURCE1} %{buildroot}/etc/init.d/%{name}
%{strip}

%preun
/usr/sbin/remove_initd nginx || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/init.d/nginx
/etc/nginx
/srv/nginx
/usr/sbin/nginx

%changelog
* Tue Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.0.8-1
- Upgrade to 1.0.8
- Optimize for size

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.7.67-1
- Initial version
