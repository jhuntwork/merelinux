Summary: Fcron Periodical Command Scheduler
Name: fcron
Version: 3.0.6
Release: 3
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://fcron.free.fr
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.src.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/fcron/fcron.init

BuildRequires: digest(sha1:%{SOURCE0}) = 6b0a886931d9a89c65df33228384b07d672238bf
BuildRequires: digest(sha1:%{SOURCE1}) = 0ea2b2a3678a9296ae5ec119d426f1eb25ca2f7c
BuildRequires: Linux-PAM-devel
BuildRequires: vim
BuildRequires: postfix
BuildRequires: lsb-bootscripts

%description
Fcron is a periodical command scheduler which aims at replacing Vixie Cron

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --with-boot-install=no
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/{pam.d,init.d}
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/fcron
rm -f %{buildroot}/etc/pam.conf
cat > %{buildroot}/etc/pam.d/fcron << "EOF"
account         required        pam_unix.so
auth            required        pam_permit.so
session         required        pam_permit.so
EOF
cat > %{buildroot}/etc/pam.d/fcrontab << "EOF"
account         required        pam_permit.so
auth            required        pam_permit.so
session         required        pam_permit.so
EOF
ln -sv fcrontab %{buildroot}/usr/bin/crontab
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install_initd fcron &>/dev/null || /bin/true

%preun
/usr/sbin/remove_initd fcron &>/dev/null || /bin/true

%files
%defattr(-,root,root)
%config /etc/init.d/fcron
%config /etc/pam.d/fcron
%config /etc/pam.d/fcrontab
/usr/sbin/fcron
/usr/share/doc/fcron-3.0.6
/usr/share/man/fr/man1/*.bz2
/usr/share/man/fr/man3/*.bz2
/usr/share/man/fr/man5/*.bz2
/usr/share/man/fr/man8/*.bz2
/usr/share/man/man1/*.bz2
/usr/share/man/man3/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man8/*.bz2
%defattr(-,root,fcron)
%config /etc/fcron.allow
%config /etc/fcron.conf
%config /etc/fcron.deny
/usr/bin/fcronsighup
%defattr(-,fcron,fcron)
/usr/bin/crontab
/usr/bin/fcrontab
/usr/bin/fcrondyn
/var/spool/fcron

%changelog
* Thu Nov 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-3
- Better management of configs
- Optimize for size

* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-2
- Fix issues with PAM modules

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-1
- Initial version
