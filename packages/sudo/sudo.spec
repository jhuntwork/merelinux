Summary: Sudo
Name: sudo
Version: 1.8.1p1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.sudo.ws/sudo
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 000c156a82216f08db743928a70c0b1990b4b32e
BuildRequires: Linux-PAM-devel
BuildRequires: zlib-devel

%description
Sudo (su "do") allows a system administrator to delegate authority to give
certain users (or groups of users) the ability to run some (or all) commands
as root or another user while providing an audit trail of the commands and
their arguments.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib} \
  --with-ignore-dot \
  --with-all-insults \
  --enable-shell-sets-home \
  --with-sendmail=/usr/sbin/sendmail \
  --with-editor=/usr/bin/vi \
  --disable-root-sudo
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
# Remove /usr/lib64/sudoers.so for now
rm -rf %{buildroot}/usr/include
# Comment out the inclusion of the non-existent /etc/sudoers.d directory
sed -i 's@^#include@#&@' %{buildroot}/etc/sudoers
# Add a PAM definition
install -dv %{buildroot}/etc/pam.d/
cat >%{buildroot}/etc/pam.d/sudo << 'EOF'
# Begin /etc/pam.d/sudo

auth        required        pam_unix.so
account     required        pam_unix.so
session     optional        pam_mail.so     dir=/var/mail standard
session     optional        pam_xauth.so
session     required        pam_env.so
session     required        pam_unix.so

# End /etc/pam.d/sudo
EOF
%{compress_man}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/sudoers
%config /etc/pam.d/sudo
/usr/bin/sudo
/usr/bin/sudoedit
/usr/bin/sudoreplay
/usr/%{_lib}/sudo_noexec.so
/usr/%{_lib}/sudoers.so
/usr/sbin/visudo
/usr/share/doc/sudo
/usr/share/man/man5/*
/usr/share/man/man8/*

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.1p1-1
- Upgrade to 1.8.1p1. Fix issues with default sudoers file and add a missing PAM config.

* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.4p2-1
- Initial version
