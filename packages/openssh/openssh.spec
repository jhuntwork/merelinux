Summary: OpenSSH
Name: openssh
Version: 5.5p1
Release: 1
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.com
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/sshd.init

Requires: base-layout, glibc, openssl, Linux-PAM, zlib
BuildRequires: digest(%{SOURCE0}) = 88633408f4cb1eb11ec7e2ec58b519eb
BuildRequires: digest(%{SOURCE1}) = 85413f16db7f2b66af700fb54df35302
BuildRequires: openssl-devel, zlib-devel

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
make

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
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.5p1-1
- Upgraded to 5.5p1 and added support for lsb bootscripts

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.4p1-1
- Initial version
