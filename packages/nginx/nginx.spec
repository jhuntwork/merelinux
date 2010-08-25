Summary: nginx HTTP Server
Name: nginx
Version: 0.7.67
Release: 1
Group: Services
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://nginx.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}.init

BuildRequires: digest(%{SOURCE0}) = b6e175f969d03a4d3c5643aaabc6a5ff
BuildRequires: digest(%{SOURCE1}) = 84a8e0f89f0b1c8e4f690715d153a5e9
BuildRequires: pcre-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
nginx [engine x] is a HTTP and reverse proxy server, as well as a mail proxy
server

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
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
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m0754 %{SOURCE1} %{buildroot}/etc/init.d/%{name}

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
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.7.67-1
- Initial version
