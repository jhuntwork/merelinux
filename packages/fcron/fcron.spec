Summary: Fcron Periodical Command Scheduler
Name: fcron
Version: 3.0.6
Release: 2
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://fcron.free.fr
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.src.tar.gz
Source1: http://dev.lightcube.us/sources/%{name}/%{name}.init

BuildRequires: digest(%{SOURCE0}) = 69ebcb41921e2a282f41ebecb3a27053
BuildRequires: digest(%{SOURCE1}) = 5010955c85fa12916e7a2608aa973b12
BuildRequires: Linux-PAM-devel
BuildRequires: postfix

%description
Fcron is a periodical command scheduler which aims at replacing Vixie Cron

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --localstatedir=/var \
  --with-boot-install=no
make

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

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install_initd fcron

%preun
/usr/sbin/remove_initd fcron

%files
%defattr(-,root,root)
/etc/init.d/fcron
/etc/pam.d/fcron
/etc/pam.d/fcrontab
/usr/sbin/fcron
/usr/share/doc/fcron-3.0.6
/usr/share/man/fr/man1/*
/usr/share/man/fr/man3/*
/usr/share/man/fr/man5/*
/usr/share/man/fr/man8/*
/usr/share/man/man1/*
/usr/share/man/man3/*
/usr/share/man/man5/*
/usr/share/man/man8/*
%defattr(-,root,fcron)
/etc/fcron.allow
/etc/fcron.conf
/etc/fcron.deny
/usr/bin/fcronsighup
%defattr(-,fcron,fcron)
/usr/bin/crontab
/usr/bin/fcrontab
/usr/bin/fcrondyn
/var/spool/fcron

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-2
- Fix issues with PAM modules

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-1
- Initial version
