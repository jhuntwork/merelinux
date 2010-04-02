Summary: Linux-PAM (Pluggable Authentication Modules for Linux)
Name: Linux-PAM
Version: 1.1.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.kernel.org/pub/linux/%{_lib}s/pam/
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-docs.tar.bz2

Requires: base-layout, glibc, cracklib
BuildRequires: digest(%{SOURCE0}) = 9b3d952b173d5b9836cbc7e8de108bee
BuildRequires: digest(%{SOURCE1}) = a8f77330be4a6bc73e0e584a599649b0

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
tar -xf %{SOURCE1} --strip-components=1
./configure \
  --docdir=/usr/share/doc/%{name}-%{version} \
  --libdir=/%{_lib} \
  --sbindir=/%{_lib}/security \
  --enable-read-both-confs
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
/%{_lib}/libpam.so.0.82.2
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
/usr/include/security
/usr/share/man/man3/*

%changelog
* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.1-1
- Upgrade to 1.1.1

* Sun Nov 01 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-2
- Added the /etc/pam.d directory

* Sat Oct 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.0-1
- Initial version
