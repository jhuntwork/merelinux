Summary: The shadow tool suite
Name: shadow
Version: 4.1.4.2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://pkg-shadow.alioth.debian.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, cracklib, Linux-PAM
BuildRequires: digest(%{SOURCE0}) = d593a9cab93c48ee0a6ba056db8c1997
BuildRequires: cracklib-devel, Linux-PAM-devel

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
sed -i 's@DICTPATH.*@DICTPATH\t/%{_lib}/cracklib/pw_dict@' \
    etc/login.defs
./configure \
  --sysconfdir=/etc \
  --with-libcrack
make

%install
make DESTDIR=%{buildroot} install
mv -v %{buildroot}/usr/bin/passwd %{buildroot}/bin
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/login
/bin/passwd
/bin/su
/etc/default/useradd
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
* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1.4.2-1
- Initial version
