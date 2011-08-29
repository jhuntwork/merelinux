Summary: Linux-PAM (Pluggable Authentication Modules for Linux)
Name: Linux-PAM
Version: 1.1.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/lib/pam
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 4634b09f9e059f384ce69dbaa4a67f88bef5cf7b
BuildRequires: cracklib-devel
BuildRequires: db-devel
BuildRequires: flex-devel
BuildRequires: zlib-devel

%description
Linux-PAM (Pluggable Authentication Modules for Linux) is a suite of shared
libraries that enable the local system administrator to choose how
applications authenticate users.

%package devel
Summary: Libraries, headers and documentation for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libaries, headers and documentation for developing with %{_name}

%prep
%setup -q

%build
./configure \
  --docdir=/usr/share/doc/%{name}-%{version} \
  --libdir=/%{_lib} \
  --sbindir=/%{_lib}/security \
  --enable-read-both-confs \
  pam_cv_ld_no_undefined=no
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/etc/pam.d
%{compress_man}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/environment
%dir /etc/pam.d
/etc/security
/%{_lib}/libpam.so.0
/%{_lib}/libpam.so.0.83.1
/%{_lib}/libpam_misc.so.0
/%{_lib}/libpam_misc.so.0.82.0
/%{_lib}/libpamc.so.0
/%{_lib}/libpamc.so.0.82.1
/%{_lib}/security
/usr/share/doc/%{name}-%{version}
/usr/share/man/man5/*
/usr/share/man/man8/*

%files devel
%defattr(-,root,root)
/%{_lib}/libpamc.so
/%{_lib}/libpam_misc.so
/%{_lib}/libpam.so
/%{_lib}/libpam.la
/%{_lib}/libpam_misc.la
/%{_lib}/libpamc.la
/usr/include/security
/usr/share/man/man3/*

%changelog
* Wed Jul 27 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.4-1
- Upgrade to 1.1.4

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.3-1
- Upgrade to 1.1.3

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.1-1
- Upgrade to 1.1.1

* Sun Nov 01 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-2
- Added the /etc/pam.d directory

* Sat Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-1
- Initial version
