Summary: rpm package manager
Name: rpm
Version: 5.1.9
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.pcre.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, bzip2, beecrypt, openssl, pcre, popt, neon, expat, zlib
BuildRequires: digest(%{SOURCE0}) = 2b6ff8f7abb1fe919402f00cc0ca56f7
BuildRequires: beecrypt-devel, openssl-devel, Python-devel, pcre-devel, popt-devel, neon-devel, expat-devel, zlib-devel, bzip2-devel

%description
RPM is a powerful and mature command-line driven package management system
capable of installing, uninstalling, verifying, querying, and updating
Unix software packages.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for using %{name} with Python
Group: Development/Libraries
Requires: %{name}, Python

%description python
Libraries for using %{name} with Python

%prep
%setup -q

%build
%ifarch x86_64
sed -i '/^%%_lib/s/lib$/lib64/' macros.in
%endif
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-openssl=yes \
  --with-python=yes \
  --with-pcre=external \
  --with-neon=external \
  --with-bzip2=external \
  --with-lua=internal \
  --with-xc=internal \
  --with-db-tools-integrated
make

%install
make DESTDIR=%{buildroot} install
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/gendiff
/usr/bin/rpm
/usr/bin/rpm2cpio
/usr/bin/rpmbuild
/usr/bin/rpmcache
/usr/bin/rpmconstant
/usr/bin/rpmdigest
/usr/bin/rpmgrep
/usr/bin/rpmmtree
/usr/bin/rpmrepo
/usr/bin/rpmspecdump
/usr/bin/rpmwget
/usr/lib/rpm
/usr/%{_lib}/librpm-5.0.so
/usr/%{_lib}/librpmbuild-5.0.so
/usr/%{_lib}/librpmconstant-5.0.so
/usr/%{_lib}/librpmdb-5.0.so
/usr/%{_lib}/librpmio-5.0.so
/usr/%{_lib}/librpmmisc-5.0.so
/usr/share/man/*/man8/*
/usr/share/man/man1/gendiff.1
/usr/share/man/man1/rpmgrep.1
/usr/share/man/man8/rpm.8
/usr/share/man/pl/man1/gendiff.1
/usr/share/man/man8/rpm2cpio.8
/usr/share/man/man8/rpmbuild.8
/usr/share/man/man8/rpmcache.8
/usr/share/man/man8/rpmconstant.8
/usr/share/man/man8/rpmdeps.8
/usr/share/man/man8/rpmgraph.8
/usr/share/man/man8/rpmmtree.8

%files devel
%defattr(-,root,root)
/usr/include/rpm
/usr/%{_lib}/pkgconfig/rpm.pc
/usr/%{_lib}/librpm.a
/usr/%{_lib}/librpm.la
/usr/%{_lib}/librpm.so
/usr/%{_lib}/librpmbuild.a
/usr/%{_lib}/librpmbuild.la
/usr/%{_lib}/librpmbuild.so
/usr/%{_lib}/librpmconstant.a
/usr/%{_lib}/librpmconstant.la
/usr/%{_lib}/librpmconstant.so
/usr/%{_lib}/librpmdb.a
/usr/%{_lib}/librpmdb.la
/usr/%{_lib}/librpmdb.so
/usr/%{_lib}/librpmio.a
/usr/%{_lib}/librpmio.la
/usr/%{_lib}/librpmio.so
/usr/%{_lib}/librpmmisc.a
/usr/%{_lib}/librpmmisc.la
/usr/%{_lib}/librpmmisc.so

%files python
%defattr(-,root,root)
/usr/%{_lib}/python2.6/site-packages/rpm

%changelog
* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-2
- Fixes to python subpackage
- Use internal db, lua and xc and external bzip2

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-1
- Initial version
