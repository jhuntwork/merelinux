Summary: Sudo
Name: sudo
Version: 1.7.4p2
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.sudo.ws/sudo
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, Linux-PAM, zlib
BuildRequires: digest(%{SOURCE0}) = 80f3a2506f0ec3e2d75e7d17d95f5341
BuildRequires: Linux-PAM-devel, zlib-devel

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
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/sudoers
/usr/bin/sudo
/usr/bin/sudoedit
/usr/bin/sudoreplay
/usr/%{_lib}/sudo_noexec.so
/usr/sbin/visudo
/usr/share/doc/sudo
/usr/share/man/man5/sudoers.5
/usr/share/man/man8/sudo.8
/usr/share/man/man8/sudoedit.8
/usr/share/man/man8/sudoreplay.8
/usr/share/man/man8/visudo.8

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.4p2-1
- Initial version
