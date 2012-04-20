Summary: Sudo
Name: sudo
Version: 1.8.3p1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.sudo.ws/sudo
Source0: http://www.sudo.ws/sudo/dist/sudo-1.8.3p1.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 2a7ad912aa8a31706796e5bff8813e4fc7505333
BuildRequires: Linux-PAM-devel
BuildRequires: zlib-devel

%description
Sudo (su "do") allows a system administrator to delegate authority to give
certain users (or groups of users) the ability to run some (or all) commands
as root or another user while providing an audit trail of the commands and
their arguments.

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
sed -i "/sys\/select\.h/s@.*@&\n# define NFDBITS		__NFDBITS\n#define __NFDBITS	(8 * sizeof(unsigned long))\n# define howmany(x, y)	(((x) + ((y) - 1)) / (y))@" plugins/sudoers/sudoreplay.c src/exec_pty.c src/exec.c

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/lib \
  --libexecdir=/usr/lib \
  --with-ignore-dot \
  --disable-nls \
  --enable-shell-sets-home \
  --with-sendmail=/usr/sbin/sendmail \
  --with-editor=/usr/bin/vi \
  --disable-root-sudo
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
# Remove /usr/lib64/sudoers.so for now
rm -rf %{buildroot}/usr/include
rm -rf %{buildroot}/usr/share/man
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
%{strip}
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
/usr/lib/sudo_noexec.so
/usr/lib/sudoers.so
/usr/sbin/visudo

%files extras
%defattr(-,root,root)
/usr/share/doc/sudo

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.3p1-1
- Initial version
