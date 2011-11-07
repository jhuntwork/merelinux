Summary: rsync
Name: rsync
Version: 3.0.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.samba.org/rsync
Source0: http://rsync.samba.org/ftp/rsync/src/rsync-3.0.9.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/rsync/rsyncd.init

BuildRequires: digest(sha1:%{SOURCE0}) = c64c8341984aea647506eb504496999fd968ddfc
BuildRequires: digest(sha1:%{SOURCE1}) = 9ef399853fcdf44fc1fbef5378aa359ab76e2c85
BuildRequires: popt-devel

%description
rsync is an open source utility that provides fast incremental file transfer.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr 
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/init.d
install -m 754 %{SOURCE1} %{buildroot}/etc/init.d/rsyncd
%{compress_man}
%{strip}
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
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.9-1
- Upgrade to 3.0.9
- Optimize for size

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.8-1
- Upgrade to 3.0.8
- Fix issue with restart in init script

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.7-1
- Initial version
