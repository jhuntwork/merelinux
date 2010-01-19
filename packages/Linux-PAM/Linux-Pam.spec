Summary: Linux-PAM (Pluggable Authentication Modules for Linux)
Name: Linux-PAM
Version: 1.1.0
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/%{_lib}s/pam/
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, cracklib

%description
Linux-PAM (Pluggable Authentication Modules for Linux) is a suite of shared
libraries that enable the local system administrator to choose how
applications authenticate users.

%package devel
Summary: Libraries, headers and documentation for developing with %{_name}
Requires: %{_name}
Group: Development/Libs

%description devel
Libaries, headers and documentation for developing with %{_name}

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/%{_lib} --sbindir=/%{_lib}/security \
  --enable-securedir=/%{_lib}/security --enable-read-both-confs
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot} -name "*.la" -exec rm -vf '{}' \;
install -dv %{buildroot}/etc/pam.d
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/environment
%dir /etc/pam.d
/etc/security
/%{_lib}/libpam.so.0
/%{_lib}/libpam.so.0.82.1
/%{_lib}/libpam_misc.so.0
/%{_lib}/libpam_misc.so.0.82.0
/%{_lib}/libpamc.so.0
/%{_lib}/libpamc.so.0.82.1
/%{_lib}/security
/usr/share/doc/Linux-PAM
/usr/share/man/man5/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/%{_lib}/libpamc.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpam.so
/usr/include/security
/usr/share/man/man3/*

%changelog
* Sun Nov 01 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-2
- Added the /etc/pam.d directory

* Sat Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-1
- Initial version
