Summary: OpenSSH
Name: openssh
Version: 5.9p1
Release: 1
Group: Services
License: BSD
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.openssh.com
Source0: http://openbsd.mirrors.hoobly.com/OpenSSH/portable/%{name}-%{version}.tar.gz
Source1: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/openssh/sshd.init
Source2: https://raw.github.com/jhuntwork/LightCube-OS/master/packages/openssh/sshd.pam

Requires(post): lsb-bootscripts
Requires(post): initd-tools
BuildRequires: digest(sha1:%{SOURCE0}) = ac4e0055421e9543f0af5da607a72cf5922dcc56
BuildRequires: digest(sha1:%{SOURCE1}) = 456397fa958e371a1c581eade51295596d07295c
BuildRequires: digest(sha1:%{SOURCE2}) = 976f40bf2ebeb36e0e3b730ceeb2246d6637e401
BuildRequires: Linux-PAM-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
OpenSSH is a free version of the SSH connectivity tools.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%{config_musl}
sed -i '/in_systm\.h/d' includes.h defines.h misc.c clientloop.c readconf.c servconf.c
sed -i "/time\.h/s@.*@&\n#include <sys/time\.h>@" misc.c
sed -i "/misc\.h/s@.*@&\n# define NFDBITS                __NFDBITS\n#define __NFDBITS    (8 * sizeof(unsigned long))\n# define howmany(x, y)     (((x) + ((y) - 1)) / (y))@" channels.c packet.c sshconnect.c sshd.c sftp-server.c ssh-keyscan.c ssh-pkcs11-helper.c ssh-agent.c
sed -i "/sys\/socket\.h/s@.*@&\n#include <sys/param\.h>@" sshd.c
sed -i "/time\.h/s@.*@&\n#include <sys/time.h>@" loginrec.c

%build
export CFLAGS='-D_BSD_SOURCE -Os -pipe'
./configure \
  --prefix=/usr \
  --sysconfdir=/etc/ssh \
  --datadir=/usr/share/sshd \
  --libexecdir=/usr/sbin \
  --with-pam \
  --with-md5-passwords \
  --with-mantype=man \
  --with-privsep-path=/var/lib/sshd \
  --disable-utmpx \
  --disable-lastlog \
  --without-zlib-version-check
sed -i '/USE_BTMP/d' config.h
make CC='gcc -Werror=implicit-function-declaration'

%install
make DESTDIR=%{buildroot} install
install -d %{buildroot}/var/lib/sshd
install -d %{buildroot}/etc/pam.d
install -d %{buildroot}/etc/init.d
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/sshd
install -m644 %{SOURCE2} %{buildroot}/etc/pam.d/sshd
sed -i '/UsePAM/s@^.*@UsePAM yes@' %{buildroot}/etc/ssh/sshd_config
%{compress_man}
%{strip}

%post
/usr/sbin/install_initd sshd 2>/dev/null || /bin/true
if [ ! -f /etc/ssh/ssh_host_key ] ; then
   /usr/bin/ssh-keygen -t rsa1 -f /etc/ssh/ssh_host_key -N "" >/dev/null 2>&1
fi
if [ ! -f /etc/ssh/ssh_host_rsa_key ] ; then
   /usr/bin/ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N "" >/dev/null 2>&1
fi
if [ ! -f /etc/ssh/ssh_host_dsa_key ] ; then
   /usr/bin/ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N "" >/dev/null 2>&1
fi
if [ ! -f /etc/ssh/ssh_host_ecdsa_key ] ; then
   /usr/bin/ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N "" >/dev/null 2>&1
fi

%preun
/usr/sbin/remove_initd sshd 2>/dev/null || /bin/true

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
%dir /var/lib/sshd

%files extras
%defattr(-,root,root)
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.9p1-1
- Initial version
