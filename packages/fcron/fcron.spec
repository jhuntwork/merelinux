Summary: Fcron Periodical Command Scheduler
Name: fcron
Version: 3.0.6
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://fcron.free.fr
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.src.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}.init

BuildRequires: digest(%{SOURCE0}) = 69ebcb41921e2a282f41ebecb3a27053
BuildRequires: digest(%{SOURCE1}) = 5010955c85fa12916e7a2608aa973b12
BuildRequires: Linux-PAM-devel

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
mv %{buildroot}/etc/pam.conf %{buildroot}/etc/pam.d/fcron
ln -sv fcrontab %{buildroot}/usr/bin/crontab
install -dv %{buildroot}/var/spool/fcron

%clean
rm -rf %{buildroot}

%post
/usr/sbin/install_initd fcron

%preun
/usr/sbin/remove_initd fcron

%files
%defattr(-,root,root)
/etc/fcron.allow
/etc/fcron.conf
/etc/fcron.deny
/etc/init.d/fcron
/etc/pam.d/fcron
/usr/bin/crontab
/usr/bin/fcrondyn
/usr/bin/fcronsighup
/usr/bin/fcrontab
/usr/sbin/fcron
/usr/share/doc/fcron-3.0.6
/usr/share/man/fr/man1/fcrondyn.1
/usr/share/man/fr/man1/fcrontab.1
/usr/share/man/fr/man3/bitstring.3
/usr/share/man/fr/man5/fcron.conf.5
/usr/share/man/fr/man5/fcrontab.5
/usr/share/man/fr/man8/fcron.8
/usr/share/man/man1/fcrondyn.1
/usr/share/man/man1/fcrontab.1
/usr/share/man/man3/bitstring.3
/usr/share/man/man5/fcron.conf.5
/usr/share/man/man5/fcrontab.5
/usr/share/man/man8/fcron.8
%defattr(-,fcron,fcron)
/var/spool/fcron

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.0.6-1
- Initial version
