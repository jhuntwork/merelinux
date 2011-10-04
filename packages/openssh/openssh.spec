Summary: OpenSSH
Name: openssh
Version: 5.8p2
Release: 3
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.com
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: https://dev.lightcube.us/svn/lightcubeos/!svn/bc/427/lightcube_os/trunk/packages/%{name}/sshd.init

Requires(post): lsb-bootscripts
Requires(post): initd-tools
Requires(post): base-files
BuildRequires: digest(sha1:%{SOURCE0}) = 64798328d310e4f06c9f01228107520adbc8b3e5
BuildRequires: digest(sha1:%{SOURCE1}) = 197058b8edd71a82d3e5cc708326a8b601189c5b
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
OpenSSH is a free version of the SSH connectivity tools.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc/ssh \
  --datadir=/usr/share/sshd \
  --libexecdir=/usr/sbin \
  --with-md5-passwords \
  --with-privsep-path=/var/lib/sshd
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/var/lib/sshd
install -dv %{buildroot}/etc/{pam.d,init.d}
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/sshd
cat > %{buildroot}/etc/pam.d/sshd << "EOF"
# Begin /etc/pam.d/sshd

auth        requisite      pam_nologin.so
auth        required       pam_securetty.so
auth        required       pam_unix.so
account     required       pam_access.so
account     required       pam_unix.so
session     required       pam_env.so
session     required       pam_motd.so
session     required       pam_limits.so
session     optional       pam_mail.so      dir=/var/mail standard
session     optional       pam_lastlog.so
session     required       pam_unix.so
password    required       pam_cracklib.so  retry=3
password    required       pam_unix.so      md5 shadow use_authtok

# End /etc/pam.d/sshd
EOF

%post
/usr/sbin/install_initd sshd
if [ ! -f /etc/ssh/ssh_host_key ] ; then
   /usr/bin/ssh-keygen -t rsa1 -f /etc/ssh/ssh_host_key -N "" &>/dev/null
fi
if [ ! -f /etc/ssh/ssh_host_rsa_key ] ; then
   /usr/bin/ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N "" &>/dev/null
fi
if [ ! -f /etc/ssh/ssh_host_dsa_key ] ; then
   /usr/bin/ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N "" &>/dev/null
fi
if [ ! -f /etc/ssh/ssh_host_ecdsa_key ] ; then
   /usr/bin/ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N "" &>/dev/null
fi

%preun
/usr/sbin/remove_initd sshd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/pam.d/sshd
/etc/init.d/sshd
/etc/ssh
/usr/bin/scp
/usr/bin/sftp
/usr/bin/slogin
/usr/bin/ssh*
/usr/sbin/sftp-server
/usr/sbin/ssh*
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*
/var/lib/sshd

%changelog
* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.8p2-3
- Fix syntax errors in %post scripts

* Mon Aug 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.8p2-2
- Improve sshd.init script, shutdown behavior

* Sun Aug 28 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.8p2-1
- Upgrade to 5.8p2
- Kill asctive ssh connections on shutdown or reboot

* Sat Sep 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.5p1-2
- Add host keys on install, if they don't exist

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.5p1-1
- Upgraded to 5.5p1 and added support for lsb bootscripts

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.4p1-1
- Initial version
