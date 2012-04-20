Summary: The shadow tool suite
Name: shadow
Version: 4.1.4.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pkg-shadow.alioth.debian.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = ad9b85b5531ce8e68f4695efc4ac53ba7266269e
BuildRequires: Linux-PAM-devel

%description
Shadow provides a suite of tools for managing system users, groups and passwords 

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
# Don't build lastlog
sed -i 's/lastlog$(EXEEXT) //' src/Makefile.in
sed -i -e '/lastlog\.h/d' -e '219,224d' lib/prototypes.h
sed -i -e 's/log\.c//' \
  -e '/log\.Po/d' \
  -e 's@ log\.\$(OBJEXT)@@' \
  libmisc/Makefile.in
sed -i "/stdio\.h/s@.*@&\n#include <sys/socket.h>@" libmisc/utmp.c
#sed -i -e 's/log\.c//' \
  #-e 's/utmp\.c//' \
  #-e '/utmp\.Po/d' \
  #-e 's@ utmp\.\$(OBJEXT)@@' \
  #libmisc/Makefile.in
mv libmisc/log.c libmisc/log.c.bak
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD SHA512@' \
       -e 's@/var/spool/mail@/var/mail@' etc/login.defs
# Kill usage of get/setusershell for now
sed -i -e '149 s@.*@/\* &@' -e '158 s@.*@& \*/@' src/su.c

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --sysconfdir=/etc \
  --with-libpam \
  --disable-nls \
  --without-nscd ac_cv_func_l64a=yes \
  ac_cv_member_struct_utmp_ut_addr_v6=no
sed -i -e 's/#define RUSEROK 0//' config.h
make

%install
make DESTDIR=%{buildroot} install
mv %{buildroot}/usr/bin/passwd %{buildroot}/bin
for FUNCTION in LASTLOG_ENAB MAIL_CHECK_ENAB \
                PORTTIME_CHECKS_ENAB CONSOLE \
                MOTD_FILE NOLOGINS_FILE PASS_MIN_LEN \
                SU_WHEEL_ONLY MD5_CRYPT_ENAB \
                CONSOLE_GROUPS ENVIRON_FILE \
                ULIMIT ENV_TZ ENV_HZ ENV_SUPATH \
                ENV_PATH QMAIL_DIR MAIL_DIR MAIL_FILE \
                CHFN_AUTH FAILLOG_ENAB QUOTAS_ENAB FTMP_FILE \
                OBSCURE_CHECKS_ENAB CRACKLIB_DICTPATH \
                PASS_CHANGE_TRIES PASS_ALWAYS_WARN ISSUE_FILE
do
    sed -i "s/^$FUNCTION/# &/" %{buildroot}/etc/login.defs
done
cat > %{buildroot}/etc/pam.d/login << "EOF"
# Begin /etc/pam.d/login

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
password    required       pam_unix.so      sha512 shadow use_authtok

# End /etc/pam.d/login
EOF
cat > %{buildroot}/etc/pam.d/passwd << "EOF"
# Begin /etc/pam.d/passwd

password    required       pam_unix.so      sha512 shadow use_authtok

# End /etc/pam.d/passwd
EOF
cat > %{buildroot}/etc/pam.d/su << "EOF"
# Begin /etc/pam.d/su

auth        sufficient      pam_rootok.so
auth        required        pam_unix.so
account     required        pam_unix.so
session     optional        pam_mail.so     dir=/var/mail standard
session     optional        pam_xauth.so
session     required        pam_env.so
session     required        pam_unix.so

# End /etc/pam.d/su
EOF
cat > %{buildroot}/etc/pam.d/chage << "EOF"
# Begin /etc/pam.d/chage

auth        sufficient      pam_rootok.so
auth        required        pam_unix.so
account     required        pam_unix.so
session     required        pam_unix.so
password    required        pam_permit.so

# End /etc/pam.d/chage
EOF
for PROGRAM in chfn chgpasswd chpasswd chsh groupadd groupdel \
               groupmems groupmod newusers useradd userdel usermod
do
    install -v -m644 %{buildroot}/etc/pam.d/chage %{buildroot}/etc/pam.d/$PROGRAM
    sed -i "s/chage/$PROGRAM/" %{buildroot}/etc/pam.d/$PROGRAM
done
cat > %{buildroot}/etc/pam.d/other << "EOF"
# Begin /etc/pam.d/other

auth        required        pam_deny.so
auth        required        pam_warn.so
account     required        pam_deny.so
account     required        pam_warn.so
password    required        pam_deny.so
password    required        pam_warn.so
session     required        pam_deny.so
session     required        pam_warn.so

# End /etc/pam.d/other
EOF
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/login
/bin/passwd
/bin/su
%config /etc/default/useradd
%config /etc/login.defs
%dir /etc/pam.d
%config /etc/pam.d/chage
%config /etc/pam.d/chfn
%config /etc/pam.d/chgpasswd
%config /etc/pam.d/chpasswd
%config /etc/pam.d/chsh
%config /etc/pam.d/groupadd
%config /etc/pam.d/groupdel
%config /etc/pam.d/groupmems
%config /etc/pam.d/groupmod
%config /etc/pam.d/login
%config /etc/pam.d/newusers
%config /etc/pam.d/other
%config /etc/pam.d/passwd
%config /etc/pam.d/su
%config /etc/pam.d/useradd
%config /etc/pam.d/userdel
%config /etc/pam.d/usermod
/sbin/nologin
/usr/bin/chage
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/expiry
/usr/bin/faillog
/usr/bin/gpasswd
/usr/bin/lastlog
/usr/bin/newgrp
/usr/bin/sg
/usr/sbin/chgpasswd
/usr/sbin/chpasswd
/usr/sbin/groupadd
/usr/sbin/groupdel
/usr/sbin/groupmems
/usr/sbin/groupmod
/usr/sbin/grpck
/usr/sbin/grpconv
/usr/sbin/grpunconv
/usr/sbin/logoutd
/usr/sbin/newusers
/usr/sbin/pwck
/usr/sbin/pwconv
/usr/sbin/pwunconv
/usr/sbin/useradd
/usr/sbin/userdel
/usr/sbin/usermod
/usr/sbin/vigr
/usr/sbin/vipw

%files extras
%defattr(-,root,root)
/usr/share/man/man1/*.bz2
/usr/share/man/man3/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man8/*.bz2

%changelog
* Mon Jan 30 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.4.3-1
- Initial version
