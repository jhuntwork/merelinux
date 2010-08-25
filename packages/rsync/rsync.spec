Summary: rsync
Name: rsync
Version: 3.0.7
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.samba.org/rsync
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}d.init

BuildRequires: digest(%{SOURCE0}) = b53525900817cf1ba7ad3a516ab5bfe9
BuildRequires: digest(%{SOURCE1}) = 2ea2a9f99f1bde5905e8b88c75127974
BuildRequires: popt-devel

%description
rsync is an open source utility that provides fast incremental file transfer.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr 
make

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m 754 %{SOURCE1} %{buildroot}/etc/init.d/rsyncd
cat > %{buildroot}/etc/rsyncd.conf << "EOF"
# This is a placeholder for a rsyncd.conf file
# Use 'man rsyncd.conf' for configuration options
uid = rsyncd
gid = rsyncd
EOF

%preun
/usr/sbin/remove_initd rsyncd || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/rsyncd.conf
/etc/init.d/rsyncd
/usr/bin/rsync
/usr/share/man/man1/rsync.1
/usr/share/man/man5/rsyncd.conf.5

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.7-1
- Initial version
