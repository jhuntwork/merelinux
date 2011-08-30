Summary: rsync
Name: rsync
Version: 3.0.8
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.samba.org/rsync
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: https://dev.lightcube.us/svn/lightcubeos/!svn/bc/440/lightcube_os/trunk/packages/%{name}/rsyncd.init

BuildRequires: digest(sha1:%{SOURCE0}) = 10e80173c7e9ed8b8a4dc9e8fdab08402da5f08d
BuildRequires: digest(sha1:%{SOURCE1}) = 9ef399853fcdf44fc1fbef5378aa359ab76e2c85
BuildRequires: popt-devel

%description
rsync is an open source utility that provides fast incremental file transfer.

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr 
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m 754 %{SOURCE1} %{buildroot}/etc/init.d/rsyncd
%{compress_man}
cat > %{buildroot}/etc/rsyncd.conf << "EOF"
# This is a placeholder for a rsyncd.conf file
# Use 'man rsyncd.conf' for configuration options
uid = rsyncd
gid = rsyncd
EOF

%preun
/usr/sbin/remove_initd rsyncd &>/dev/null || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/rsyncd.conf
%config /etc/init.d/rsyncd
/usr/bin/rsync
/usr/share/man/man1/rsync.1.bz2
/usr/share/man/man5/rsyncd.conf.5.bz2

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.8-1
- Upgrade to 3.0.8
- Fix issue with restart in init script

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.7-1
- Initial version
