Summary: rpm package manager
Name: rpm
Version: 5.3.11
Release: 3
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.rpm5.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 65693e935a6706e3dce6e6d920f0cf50a9dca22b
BuildRequires: beecrypt-devel
BuildRequires: bzip2-devel
BuildRequires: db-devel
BuildRequires: elfutils-devel
BuildRequires: expat-devel
BuildRequires: file-devel
BuildRequires: neon-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: popt-devel
BuildRequires: python-devel
BuildRequires: readline-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
RPM is a powerful and mature command-line driven package management system
capable of installing, uninstalling, verifying, querying, and updating
Unix software packages.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}
Requires: %{name}-build >= %{version}

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for using %{name} with Python
Group: Development/Libraries
Requires: %{name} >= %{version}
Requires: Python
Requires: setuptools

%description python
Libraries for using %{name} with Python

%package build
Summary: Tools for building rpm packages
Group: Development/Utilities
Requires: %{name} >= %{version}

%description build
Tools for building rpm packages

%prep
%setup -q
cat > rpm-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed -e '/perl(MDK::Common)/d'
EOF
chmod +x rpm-req
%define __perl_requires %{_builddir}/rpm-%{version}/rpm-req

%build
%ifarch x86_64
sed -i '/^%%_lib/s/lib$/lib64/' macros/macros.in
%endif
# FHS mods
sed -i 's@_prefix}/info@_datadir}/info@' macros/macros.in
sed -i 's@_prefix}/man@_datadir}/man@' macros/macros.in
export CFLAGS="-Os -pipe"
# Use the internal (shipped) version of db due to the tight
# coupling of rpm and db - upgrading is difficult otherwise
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --disable-openmp \
  --with-bzip2=external \
  --with-expat=external \
  --with-file=external \
  --with-libelf \
  --with-lua=internal \
  --with-neon=external \
  --with-openssl \
  --with-pcre=external \
  --with-popt=external \
  --with-python \
  --without-selinux \
  --with-readline \
  --with-xz=external \
  --with-zlib
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/var/lib/rpm/{log,tmp}
install -dv %{buildroot}/etc/rpm
install -dv %{buildroot}/usr/src/rpm
echo "%%PMFLAGS   -j1" >> %{buildroot}/etc/rpm/macros
echo "%%compress_man	/usr/lib/rpm/compress_man.sh %%{buildroot}" >> %{buildroot}/etc/rpm/macros
echo "%%strip		/usr/lib/rpm/strip.sh %%{buildroot}" >> %{buildroot}/etc/rpm/macros

# Add compress man helper
cat > %{buildroot}/usr/lib/rpm/compress_man.sh << "EOF"
#!/bin/bash
find "$@/usr/share/man" -type f -exec bzip2 -9 '{}' \;
for i in $(find "$@/usr/share/man" -type l) ; do
    link=$(basename `readlink $i`)
    fn=$(basename $i)
    dn=$(dirname $i)
    rm -vf $i
    ln -sv $link.bz2 "$dn/$fn.bz2"
done
EOF
chmod 0755 %{buildroot}/usr/lib/rpm/compress_man.sh

# Add strip helper
cat > %{buildroot}/usr/lib/rpm/strip.sh << "EOF"
#!/bin/bash
find ${1} -type f -exec strip --strip-unneeded -R .comment -R .note '{}' \; 2>/dev/null || /bin/true
EOF
chmod 0755 %{buildroot}/usr/lib/rpm/strip.sh

# Compress man pages
%{compress_man}
# Strip
find %{buildroot} -type f -exec strip --strip-unneeded -R .comment -R .note '{}' \; 2>/dev/null || /bin/true

# Create /etc/rpm/platform
cat > %{buildroot}/etc/rpm/platform << "EOF"
%{_target_cpu}-%{_target_vendor}-%{_target_os}%{?_gnu}
noarch-%{_target_vendor}-%{_target_os}%{?_gnu}
%{_target_cpu}-.*-%{_target_os}.*
noarch-.*-%{_target_os}.*
EOF

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/rpm/
/etc/rpm/platform
/usr/bin/gendiff
/usr/bin/rpm
/usr/bin/rpm2cpio
/usr/bin/rpmconstant
/usr/bin/multiarch-dispatch
/usr/bin/multiarch-platform
/usr/%{_lib}/librpm-5.3.so
/usr/%{_lib}/librpmbuild-5.3.so
/usr/%{_lib}/librpmconstant-5.3.so
/usr/%{_lib}/librpmdb-5.3.so
/usr/%{_lib}/librpmio-5.3.so
/usr/%{_lib}/librpmmisc-5.3.so
%dir /usr/lib/rpm
%dir /usr/lib/rpm/bin
/usr/lib/rpm/bin/debugedit
/usr/lib/rpm/bin/mtree
/usr/lib/rpm/bin/rpmcache
/usr/lib/rpm/bin/rpmcmp
/usr/lib/rpm/bin/rpmdeps
/usr/lib/rpm/bin/rpmdigest
/usr/lib/rpm/bin/rpmspecdump
/usr/lib/rpm/bin/wget
/usr/lib/rpm/bin/abi-compliance-checker.pl
/usr/lib/rpm/bin/api-sanity-autotest.pl
/usr/lib/rpm/bin/chroot
/usr/lib/rpm/bin/cp
/usr/lib/rpm/bin/dbsql
/usr/lib/rpm/bin/find
/usr/lib/rpm/bin/install-sh
/usr/lib/rpm/bin/mkinstalldirs
/usr/lib/rpm/bin/rpmlua
/usr/lib/rpm/bin/rpmluac
/usr/lib/rpm/bin/sqlite3
/usr/lib/rpm/bin/lua
/usr/lib/rpm/bin/luac
/usr/lib/rpm/dbconvert.sh
/usr/lib/rpm/gem_helper.rb
/usr/lib/rpm/cpuinfo.yaml
/usr/lib/rpm/find-debuginfo.sh
/usr/lib/rpm/helpers
/usr/lib/rpm/macros
/usr/lib/rpm/macros.d
/usr/lib/rpm/perl.req
/usr/lib/rpm/qf
/usr/lib/rpm/rpm.daily
/usr/lib/rpm/rpm.log
/usr/lib/rpm/rpm.xinetd
/usr/lib/rpm/rpm2cpio
/usr/lib/rpm/rpmdb_loadcvt
/usr/lib/rpm/rpmpopt
/usr/lib/rpm/tgpg
/usr/lib/rpm/u_pkg.sh
/usr/lib/rpm/vpkg-provides.sh
/usr/lib/rpm/vpkg-provides2.sh
/usr/lib/rpm/bin/dbconvert
/usr/lib/rpm/check-multiarch-files
/usr/lib/rpm/mkmultiarch
/usr/lib/rpm/rubygems.rb
%dir /var/lib/rpm
/var/lib/rpm/DB_CONFIG
%dir /var/lib/rpm/log
%dir /var/lib/rpm/tmp
/usr/share/man/man1/gendiff.1.bz2
/usr/share/man/*/man1/gendiff.1.bz2
/usr/share/man/man1/rpmgrep.1.bz2
/usr/share/man/man8/rpm.8.bz2
/usr/share/man/*/man8/rpm.8.bz2
/usr/share/man/man8/rpm2cpio.8.bz2
/usr/share/man/*/man8/rpm2cpio.8.bz2
/usr/share/man/man8/rpmcache.8.bz2
/usr/share/man/*/man8/rpmcache.8.bz2
/usr/share/man/man8/rpmconstant.8.bz2
/usr/share/man/man8/rpmdeps.8.bz2
/usr/share/man/*/man8/rpmdeps.8.bz2
/usr/share/man/man8/rpmmtree.8.bz2
/usr/share/man/*/man8/rpmgraph.8.bz2

%files devel
%defattr(-,root,root)
/usr/include/rpm
/usr/include/multiarch-dispatch.h
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
/usr/lib/rpm/lib

%files python
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/rpm
/usr/lib/rpm/pythoneggs.py

%files build
%defattr(-,root,root)
%config /etc/rpm/macros
/usr/bin/rpmbuild
/usr/lib/rpm/brp-*
/usr/lib/rpm/check-files
/usr/lib/rpm/cross-build
/usr/lib/rpm/compress_man.sh
/usr/lib/rpm/find-lang.sh
/usr/lib/rpm/find-prov.pl
/usr/lib/rpm/find-provides.perl
/usr/lib/rpm/find-req.pl
/usr/lib/rpm/find-requires.perl
/usr/lib/rpm/macros.rpmbuild
/usr/lib/rpm/mono-find-provides
/usr/lib/rpm/mono-find-requires
/usr/lib/rpm/perldeps.pl
/usr/lib/rpm/executabledeps.sh
/usr/lib/rpm/javadeps.sh
/usr/lib/rpm/libtooldeps.sh
/usr/lib/rpm/pkgconfigdeps.sh
/usr/lib/rpm/osgideps.pl
/usr/lib/rpm/getpo.sh
/usr/lib/rpm/http.req
/usr/lib/rpm/pythondeps.sh
/usr/lib/rpm/bin/rpmrepo
/usr/lib/rpm/perl.prov
/usr/lib/rpm/php.prov
/usr/lib/rpm/php.req
/usr/lib/rpm/strip.sh
/usr/lib/rpm/vcheck
%dir /usr/src/rpm
/usr/share/man/man8/rpmbuild.8.bz2
/usr/share/man/*/man8/rpmbuild.8.bz2

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.11-3
- Remove dependency on sqlite, libxml2, xar - unused
- Add strip macro support
- Optimize for size

* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.11-2
- Fix requires for rpm-python, add dep on setuptools

* Sat Aug 20 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.11-1
- Upgrade to 5.3.11 - Fixes an issue with honoring %config directives
- Add external beecrypt since it is now mandatory

* Mon Mar 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.6-2
- Add /usr/src/rpm directory to rpm-build
- Remove dependency on external beecrypt

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.6-1
- Upgrade to 5.3.6

* Tue Sep 07 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.3-1
- Upgrade to 5.3.3

* Mon Aug 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.2-2
- Use external db

* Thu Aug 26 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.2-1
- Update to 5.3.2

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-2
- Fixes to python subpackage
- Use internal db, lua and xc and external bzip2

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-1
- Initial version
