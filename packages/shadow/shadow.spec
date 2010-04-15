Summary: The shadow tool suite
Name: shadow
Version: 4.1.4.2
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pkg-shadow.alioth.debian.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, cracklib, Linux-PAM
BuildRequires: digest(%{SOURCE0}) = d593a9cab93c48ee0a6ba056db8c1997
BuildRequires: Linux-PAM-devel

%description
%{name} provides a suite of tools for managing system users, groups and passwords 

%prep
%setup -q

%build
sed -i 's/groups$(EXEEXT) //' src/Makefile.in
find man -name Makefile.in -exec sed -i 's/groups\.1 / /' {} \;
sed -i -e 's/ ko//' -e 's/ zh_CN zh_TW//' man/Makefile.in
sed -i -e 's@#ENCRYPT_METHOD DES@ENCRYPT_METHOD MD5@' \
       -e 's@/var/spool/mail@/var/mail@' etc/login.defs
./configure \
  --sysconfdir=/etc
make

%install
make DESTDIR=%{buildroot} install
mv -v %{buildroot}/usr/bin/passwd %{buildroot}/bin
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
password    required       pam_cracklib.so  retry=3
password    required       pam_unix.so      md5 shadow use_authtok

# End /etc/pam.d/login
EOF
cat > %{buildroot}/etc/pam.d/passwd << "EOF"
# Begin /etc/pam.d/passwd

password    required       pam_cracklib.so  type=Linux retry=1 \
                                            difok=5 diffignore=23 minlen=9 \
                                            dcredit=1 ucredit=1 lcredit=1 \
                                            ocredit=1 \
                                            dictpath=/%{_lib}/cracklib/pw_dict
password    required       pam_unix.so      md5 shadow use_authtok

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
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/login
/bin/passwd
/bin/su
/etc/default
/etc/login.defs
/etc/pam.d
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
/usr/share/man/*/man1/*
/usr/share/man/*/man3/*
/usr/share/man/*/man5/*
/usr/share/man/*/man8/*
/usr/share/man/man1/*
/usr/share/man/man3/*
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog
* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.4.2-2
- Don't link directly to cracklib

* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.4.2-1
- Initial version
