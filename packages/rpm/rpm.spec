Summary: rpm package manager
Name: rpm
Version: 5.2.1
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.rpm5.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/scriptletdeps.sh
Source2: http://dev.lightcube.us/~jhuntwork/sources/%{name}/check-rpaths
Source3: http://dev.lightcube.us/~jhuntwork/sources/%{name}/check-rpaths-worker
Source4: http://dev.lightcube.us/~jhuntwork/sources/%{name}/brp-nobuilddirpath
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.1.6_macrofix.patch
Patch1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.0.3_envfix.patch
Patch2: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.1.6_tar-fix.patch
Patch3: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.1.9_no-parentdirs.patch
Patch4: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.1.9_perl-vendor.patch
Patch5: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.1.9_ordering-fix.patch
Patch6: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.2.0_parentdir-vs-requires.patch
Patch7: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.2.0_depends-fix.patch
Patch8: http://dev.lightcube.us/~jhuntwork/sources/%{name}/rpm-5.2.0_umem-fix.patch

Requires: base-layout, glibc, bzip2, beecrypt, openssl, pcre, popt, neon, expat, zlib, elfutils-libelf, file, readline, xar, xz, libxml2
BuildRequires: digest(%{SOURCE0}) = 71f825ede4a2ddc191132ae017c9a6e4
BuildRequires: digest(%{SOURCE1}) = 27dfe162f78b88d13538407dd60c68ae
BuildRequires: digest(%{SOURCE2}) = d4bee74500d8634f80529b345153516a
BuildRequires: digest(%{SOURCE3}) = 90a6ada57b7a6ed8842d6c87e484524c
BuildRequires: digest(%{SOURCE4}) = 466d42aecf322e258d50fffe09e0bcc9
BuildRequires: digest(%{PATCH0}) = b5ecaa7f29818957c322ff9b018c85b3 
BuildRequires: digest(%{PATCH1}) = c00058f24dc442f52c467f13a5b5cd70
BuildRequires: digest(%{PATCH2}) = c9b4b6366e17d1cce53e6eb33a6b2937
BuildRequires: digest(%{PATCH3}) = eae8b5767aa60a68a0512b41efa6a08d
BuildRequires: digest(%{PATCH4}) = 538e3960ddc7d45f6ecf5eac5f00f337
BuildRequires: digest(%{PATCH5}) = 1b92cf05f07ca58ce6c0feca8124ab1b
BuildRequires: digest(%{PATCH6}) = b206993c3ca04d8f27603349c44805e1
BuildRequires: digest(%{PATCH7}) = 0524bc4dd16d37ce62f668450726ae7d
BuildRequires: digest(%{PATCH8}) = c0c40b0b93ae4f286677744401074fc8
BuildRequires: beecrypt-devel, openssl-devel, Python-devel, pcre-devel, popt-devel, neon-devel, readline-devel
BuildRequires: expat-devel, zlib-devel, bzip2-devel, elfutils-devel, file-devel, libxml2-devel, xar-devel, xz-devel

%description
RPM is a powerful and mature command-line driven package management system
capable of installing, uninstalling, verifying, querying, and updating
Unix software packages.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}, %{name}-build

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for using %{name} with Python
Group: Development/Libraries
Requires: %{name}, Python

%description python
Libraries for using %{name} with Python

%package build
Summary: Tools for building rpm packages
Group: Development/Utilities
Requires: %{name}

%description build
Tools for building rpm packages

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p0
%patch6 -p1
%patch7 -p1
%patch8 -p0
sed -i 's@python_version="2.6@python_version="2.7 2.6@' configure

%build
%ifarch x86_64
sed -i '/^%%_lib/s/lib$/lib64/' macros.in
# FHS mods
sed -i 's@_prefix}/info@_datadir}/info@' macros.in
sed -i 's@_prefix}/man@_datadir}/man@' macros.in
%endif
export CFLAGS="%{CFLAGS}  -I/usr/include/xar"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-openssl \
  --with-python=yes \
  --with-pcre=external \
  --with-zlib \
  --with-neon=external \
  --with-bzip2=external \
  --with-lua=internal \
  --with-xz=external \
  --with-file=external \
  --with-xar=external \
  --without-selinux \
  --with-libelf \
  --disable-rpath \
  --disable-dependency-tracking \
  --with-db-tools-integrated
make

%install
make DESTDIR=%{buildroot} install
install -m 755 %{SOURCE1} %{buildroot}/usr/lib/rpm/scriptletdeps.sh
# Install rpath test scripts
install -m0755 %{SOURCE2} %{buildroot}/usr/lib/rpm/check-rpaths
install -m0755 %{SOURCE3} %{buildroot}/usr/lib/rpm/check-rpaths-worker
install -m0755 %{SOURCE4} %{buildroot}/usr/lib/rpm/brp-nobuilddirpath
install -dv %{buildroot}/etc/rpm
echo "%%CFLAGS    -O2 -pipe" >> %{buildroot}/etc/rpm/macros
echo "%%LDFLAGS   -s" >> %{buildroot}/etc/rpm/macros
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%dir /etc/rpm/
/usr/bin/gendiff
/usr/bin/rpm
/usr/bin/rpm2cpio
/usr/bin/rpmconstant
%dir /usr/lib/rpm
%dir /usr/lib/rpm/bin
/usr/lib/rpm/bin/db_archive
/usr/lib/rpm/bin/db_checkpoint
/usr/lib/rpm/bin/db_deadlock
/usr/lib/rpm/bin/db_dump
/usr/lib/rpm/bin/db_hotbackup
/usr/lib/rpm/bin/db_load
/usr/lib/rpm/bin/db_printlog
/usr/lib/rpm/bin/db_recover
/usr/lib/rpm/bin/db_stat
/usr/lib/rpm/bin/db_tool
/usr/lib/rpm/bin/db_upgrade
/usr/lib/rpm/bin/db_verify
/usr/lib/rpm/bin/debugedit
/usr/lib/rpm/bin/grep
/usr/lib/rpm/bin/mtree
/usr/lib/rpm/bin/rpmcache
/usr/lib/rpm/bin/rpmcmp
/usr/lib/rpm/bin/rpmdeps
/usr/lib/rpm/bin/rpmdigest
/usr/lib/rpm/bin/rpmspecdump
/usr/lib/rpm/bin/txar
/usr/lib/rpm/bin/wget
/usr/lib/rpm/cpuinfo.yaml
/usr/lib/rpm/find-debuginfo.sh
/usr/lib/rpm/helpers
/usr/lib/rpm/macros
/usr/lib/rpm/mkinstalldirs
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
/usr/%{_lib}/librpm-5.2.so
/usr/%{_lib}/librpmbuild-5.2.so
/usr/%{_lib}/librpmconstant-5.2.so
/usr/%{_lib}/librpmdb-5.2.so
/usr/%{_lib}/librpmio-5.2.so
/usr/%{_lib}/librpmmisc-5.2.so
/usr/share/man/*/man8/*
/usr/share/man/man1/gendiff.1
/usr/share/man/man1/rpmgrep.1
/usr/share/man/man8/rpm.8
/usr/share/man/pl/man1/gendiff.1
/usr/share/man/man8/rpm2cpio.8
/usr/share/man/man8/rpmcache.8
/usr/share/man/man8/rpmconstant.8
/usr/share/man/man8/rpmdeps.8
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
/usr/lib/python2.7/site-packages/rpm

%files build
%defattr(-,root,root)
/etc/rpm/macros
/usr/bin/rpmbuild
/usr/lib/rpm/install-sh
/usr/lib/rpm/brp-*
/usr/lib/rpm/check-*
/usr/lib/rpm/cross-build
/usr/lib/rpm/find-lang.sh
/usr/lib/rpm/find-prov.pl
/usr/lib/rpm/find-provides.perl
/usr/lib/rpm/find-req.pl
/usr/lib/rpm/find-requires.perl
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
/usr/lib/rpm/scriptletdeps.sh
/usr/lib/rpm/vcheck
/usr/share/man/man8/rpmbuild.8

%changelog
* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.2.1-1
- Update to 5.2.1

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-2
- Fixes to python subpackage
- Use internal db, lua and xc and external bzip2

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.1.9-1
- Initial version
