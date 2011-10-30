Summary: OpenSSH
Name: openssh
Version: 5.8p2
Release: 4
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssl.com
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/openssh/sshd.init
Source2: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/openssh/sshd.pam

Requires(post): lsb-bootscripts
Requires(post): initd-tools
BuildRequires: digest(sha1:%{SOURCE0}) = 64798328d310e4f06c9f01228107520adbc8b3e5
BuildRequires: digest(sha1:%{SOURCE1}) = 456397fa958e371a1c581eade51295596d07295c
BuildRequires: digest(sha1:%{SOURCE2}) = 976f40bf2ebeb36e0e3b730ceeb2246d6637e401
BuildRequires: openssl-devel
BuildRequires: zlib-devel
BuildRequires: groff

%description
OpenSSH is a free version of the SSH connectivity tools.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
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
install -m644 %{SOURCE2} %{buildroot}/etc/pam.d/sshd
%{compress_man}
%{strip}

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
%config /etc/pam.d/sshd
%config /etc/init.d/sshd
%dir /etc/ssh
/etc/ssh/moduli
%config /etc/ssh/ssh_config
%config /etc/ssh/sshd_config
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
* Fri Oct 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.8p2-4
- Make sshd init script even more robust when using the restart param
- Optimize for size

* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.8p2-3
- Fix %post scripts and their dependencies for package installation ordering

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
