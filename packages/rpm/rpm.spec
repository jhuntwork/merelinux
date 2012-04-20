Summary: rpm package manager
Name: rpm
Version: 5.3.11
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.rpm5.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: compress_man.sh
Patch0: rpm-musl.patch
Patch1: rpm-no-error.patch

BuildRequires: digest(sha1:%{SOURCE0}) = 65693e935a6706e3dce6e6d920f0cf50a9dca22b
BuildRequires: digest(sha1:%{SOURCE1}) = 54bf644ea5c9fc86de89916837f7534c842ce91f
BuildRequires: digest(sha1:%{PATCH0})  = c4172dab3ac1dfb58d690aeeaee6d49561f41600
BuildRequires: digest(sha1:%{PATCH1})  = 21cba0c19ba2fdb40197647f78c586db928f6f62
BuildRequires: beecrypt-devel
BuildRequires: db-devel
BuildRequires: expat-devel
BuildRequires: file-devel
BuildRequires: libelf-devel
BuildRequires: neon-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: popt-devel
#BuildRequires: python-devel
#BuildRequires: readline-devel
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

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

#%package python
#Summary: Libraries for using %{name} with Python
#Group: Development/Libraries
#Requires: %{name} >= %{version}
#Requires: Python
#Requires: setuptools

#%description python
#Libraries for using %{name} with Python

%package build
Summary: Tools for building rpm packages
Group: Development/Utilities
Requires: %{name} >= %{version}

%description build
Tools for building rpm packages

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%{config_musl}
cat > rpm-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed -e '/perl(MDK::Common)/d'
EOF
chmod +x rpm-req
%define __perl_requires %{_builddir}/rpm-%{version}/rpm-req
sed -i 's@-fstack-protector@@' configure
# FHS mods
sed -i 's@_prefix}/info@_datadir}/info@' macros/macros.in
sed -i 's@_prefix}/man@_datadir}/man@' macros/macros.in
sed -i '/^%%_usr/s,@usrprefix@,/,' macros/macros.in
sed -i '/^%%_prefix/s,@prefix@,/,' macros/macros.in

%build
#FIXME - don't use -D__musl__ - requires new patch
export CFLAGS="-D_GNU_SOURCE -D__musl__ -Os"
export LDFLAGS="--static"
./configure \
  --prefix='' \
  --disable-openmp \
  --disable-nls \
  --disable-shared \
  --enable-static \
  --enable-build-static \
  --with-expat=external \
  --with-file=external \
  --with-libelf \
  --without-lua \
  --with-neon \
  --with-openssl \
  --with-pcre=external \
  --with-popt=external \
  --without-selinux \
  --with-xz=external \
  --with-zlib
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/var/lib/rpm/tmp
install -dv %{buildroot}/etc/rpm
install -dv %{buildroot}/src/rpm
for file in `grep -lr '/usr/bin' %{buildroot}/lib/rpm` ; do
   sed -i 's@/usr/bin@/bin@g' $file
done
echo "%%PMFLAGS   -j\`cat /proc/cpuinfo | grep processor | wc -l\`" >> %{buildroot}/etc/rpm/macros
echo "%%compress_man	%%{_rpmhome}/compress_man.sh %%{buildroot}" >> %{buildroot}/etc/rpm/macros
echo "%%strip		%%{_rpmhome}/strip.sh %%{buildroot}" >> %{buildroot}/etc/rpm/macros
echo "%%config_musl	sed -i -e 's/linux-gnu/linux-musl/g' -e 's@LIBC=gnu@LIBC=musl@' \`find . -name "confi*.guess" -o -name "confi*.sub"\`" \
  >>%{buildroot}/etc/rpm/macros

# Keep log files in top /var/lib/rpm dir for consistency
sed -i 's@/log@@' %{buildroot}/var/lib/rpm/DB_CONFIG

# Add compress man helper
install -m 0755 %{SOURCE1} \
  %{buildroot}/lib/rpm/compress_man.sh

# Add strip helper
cat > %{buildroot}/lib/rpm/strip.sh << "EOF"
#!/bin/bash
find ${1} -type f -exec strip -v --strip-unneeded -R .comment -R .note '{}' \; 2>/dev/null || /bin/true
EOF
chmod 0755 %{buildroot}/lib/rpm/strip.sh

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

%clean
rm -rf %{buildroot}

%post
if [ -d "/var/lib/rpm/log/" ] ; then
    /bin/mv /var/lib/rpm/log/* /var/lib/rpm/ 2>/dev/null || /bin/true
fi

%files
%defattr(-,root,root)
%dir /etc/rpm/
/etc/rpm/platform
/bin/gendiff
/bin/rpm
/bin/rpm2cpio
/bin/rpmconstant
/bin/multiarch-dispatch
/bin/multiarch-platform
%dir /lib/rpm
%dir /lib/rpm/bin
/lib/rpm/bin/debugedit
/lib/rpm/bin/mtree
/lib/rpm/bin/rpmcache
/lib/rpm/bin/rpmcmp
/lib/rpm/bin/rpmdeps
/lib/rpm/bin/rpmdigest
/lib/rpm/bin/rpmspecdump
/lib/rpm/bin/wget
/lib/rpm/bin/chroot
/lib/rpm/bin/cp
/lib/rpm/bin/find
/lib/rpm/bin/install-sh
/lib/rpm/bin/mkinstalldirs
/lib/rpm/bin/sqlite3
/lib/rpm/macros
/lib/rpm/rpm2cpio
/lib/rpm/rpmdb_loadcvt
/lib/rpm/rpmpopt
/lib/rpm/tgpg
/lib/rpm/vcheck
%dir /lib/rpm/macros.d
%dir /var/lib/rpm
/var/lib/rpm/DB_CONFIG
%dir /var/lib/rpm/tmp

%files devel
%defattr(-,root,root)
/include/rpm
/include/multiarch-dispatch.h
/lib/pkgconfig/rpm.pc
/lib/librpm.a
/lib/librpm.la
/lib/librpmbuild.a
/lib/librpmbuild.la
/lib/librpmconstant.a
/lib/librpmconstant.la
/lib/librpmdb.a
/lib/librpmdb.la
/lib/librpmio.a
/lib/librpmio.la
/lib/librpmmisc.a
/lib/librpmmisc.la

#%files python
#%defattr(-,root,root)
#/lib/python2.7/site-packages/rpm

%files build
%defattr(-,root,root)
%config /etc/rpm/macros
/bin/rpmbuild
/lib/rpm/brp-*
/lib/rpm/check-files
/lib/rpm/cross-build
/lib/rpm/compress_man.sh
/lib/rpm/find-lang.sh
/lib/rpm/find-prov.pl
/lib/rpm/find-provides.perl
/lib/rpm/find-req.pl
/lib/rpm/find-requires.perl
/lib/rpm/macros.rpmbuild
/lib/rpm/mono-find-provides
/lib/rpm/mono-find-requires
/lib/rpm/perldeps.pl
/lib/rpm/pythoneggs.py
/lib/rpm/executabledeps.sh
/lib/rpm/javadeps.sh
/lib/rpm/libtooldeps.sh
/lib/rpm/pkgconfigdeps.sh
/lib/rpm/osgideps.pl
/lib/rpm/getpo.sh
/lib/rpm/http.req
/lib/rpm/pythondeps.sh
/lib/rpm/bin/abi-compliance-checker.pl
/lib/rpm/bin/api-sanity-autotest.pl
/lib/rpm/bin/rpmrepo
/lib/rpm/perl.prov
/lib/rpm/php.prov
/lib/rpm/php.req
/lib/rpm/strip.sh
/lib/rpm/dbconvert.sh
/lib/rpm/gem_helper.rb
/lib/rpm/cpuinfo.yaml
/lib/rpm/find-debuginfo.sh
/lib/rpm/helpers
/lib/rpm/perl.req
/lib/rpm/qf
/lib/rpm/rpm.xinetd
/lib/rpm/u_pkg.sh
/lib/rpm/vpkg-provides.sh
/lib/rpm/vpkg-provides2.sh
/lib/rpm/bin/dbconvert
/lib/rpm/check-multiarch-files
/lib/rpm/macros.d/*
/lib/rpm/mkmultiarch
/lib/rpm/rubygems.rb
%dir /src/rpm

%files extras
%defattr(-,root,root)
/lib/rpm/rpm.daily
/lib/rpm/rpm.log
/share/man/man1/gendiff.1.bz2
/share/man/man1/rpmgrep.1.bz2
/share/man/man8/rpm.8.bz2
/share/man/man8/rpm2cpio.8.bz2
/share/man/man8/rpmbuild.8.bz2
/share/man/man8/rpmcache.8.bz2
/share/man/man8/rpmconstant.8.bz2
/share/man/man8/rpmdeps.8.bz2
/share/man/man8/rpmmtree.8.bz2

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.3.11-1
- Initial version
