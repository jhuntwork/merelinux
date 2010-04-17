Summary: OpenSSH
Name: openssh
Version: 5.4p1
Release: 1
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.com
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/blfs-bootscripts/blfs-bootscripts-20090302.tar.bz2

Requires: base-layout, glibc, openssl, Linux-PAM, zlib
BuildRequires: digest(%{SOURCE0}) = da10af8a789fa2e83e3635f3a1b76f5e
BuildRequires: digest(%{SOURCE1}) = 7ee5363f223235adc54046623ffa77cd
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
install -dv %{buildroot}/etc/{pam.d,rc.d/init.d}
tar -xf %{SOURCE1}
install -m754 blfs-bootscripts-20090302/blfs/init.d/sshd \
  %{buildroot}/etc/rc.d/init.d/
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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/pam.d/sshd
/etc/rc.d/init.d/sshd
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
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.4p1-1
- Initial version
