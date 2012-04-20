Summary: Perl Progamming Language
Name: perl
Version: 5.14.2
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.perl.org
Source0: http://www.cpan.org/src/5.0/perl-5.14.2.tar.gz
Patch0: Digest_security_fix.patch

BuildRequires: digest(sha1:%{SOURCE0}) = df1549d65cdef2b20023af83ecaa2a024109a5ad
BuildRequires: digest(sha1:%{PATCH0})  = c070099859db65415cbd970bda1c99da76ba4620
BuildRequires: zlib-devel
Provides: perl
Provides: perl(Carp::Heavy)
Provides: perl(getopts.pl)
Provides: perl(bigint.pl)

%description
Perl is a feature-rich platform programming language.

%package extras
Group: Development/Languages
Summary: Documentation for perl
Requires: %{name} >= %{version}

%description extras
Documentation for perl

%prep
%setup -q
%patch0 -p1
# perl doesn't conform to POSIX sh and doesn't offer any easy workaround
mkdir bin
ln -s /bin/bash bin/sh

# we need to filter out a few auto requirements
cat > %{name}-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed \
	-e '/perl(FCGI)/d' \
	-e '/perl(Mac::BuildTools)/d' \
	-e '/perl(Mac::InternetConfig)/d' \
	-e '/perl(Tk)/d' \
	-e '/perl(Tk::Pod)/d' \
	-e '/perl(VMS::Filespec)/d' \
	-e '/perl(VMS::Stdio)/d' \
	-e '/perl(NDBM_File)/d' \
	-e '/perl(Your::Module::Here)/d' \
	-e '/perl(DBD::SQLite)/d' \
	-e '/perl(DBIx::Simple)/d'
EOF
chmod +x %{name}-req
%define __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req

%build
sed -i -e "s|BUILD_ZLIB\s*= True|BUILD_ZLIB = False|" \
       -e "s|INCLUDE\s*= ./zlib-src|INCLUDE = /usr/include|" \
       -e "s|LIB\s*= ./zlib-src|LIB = /usr/lib|" \
       cpan/Compress-Raw-Zlib/config.in
sh Configure \
  -des \
  -Dprefix=/usr \
  -Dvendorprefix=/usr           \
  -Dman1dir=/usr/share/man/man1 \
  -Dman3dir=/usr/share/man/man3 \
  -Dpager="/usr/bin/less -isR" \
  -Duseshrplib
make OPTIMIZE="-D_GNU_SOURCE -Os -pipe"

%install
make DESTDIR=%{buildroot} install
cp %{buildroot}/usr/lib/perl5/%{version}/$(uname -m)-linux/CORE/libperl.so %{buildroot}/usr/lib/
install -d %{buildroot}/usr/lib/perl5/site_perl/%{version}/$(uname -m)-linux/auto
install -d %{buildroot}/usr/lib/perl5/site_perl/%{version}/$(uname -m)-linux/Bundle
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/a2p
/usr/bin/c2ph
/usr/bin/config_data
/usr/bin/corelist
/usr/bin/cpan
/usr/bin/cpan2dist
/usr/bin/cpanp
/usr/bin/cpanp-run-perl
/usr/bin/dprofpp
/usr/bin/enc2xs
/usr/bin/find2perl
/usr/bin/h2ph
/usr/bin/h2xs
/usr/bin/instmodsh
/usr/bin/json_pp
/usr/bin/libnetcfg
/usr/bin/perl
/usr/bin/perl%{version}
/usr/bin/perlbug
/usr/bin/perldoc
/usr/bin/perlivp
/usr/bin/perlthanks
/usr/bin/piconv
/usr/bin/pl2pm
/usr/bin/pod2html
/usr/bin/pod2latex
/usr/bin/pod2man
/usr/bin/pod2text
/usr/bin/pod2usage
/usr/bin/podchecker
/usr/bin/podselect
/usr/bin/prove
/usr/bin/psed
/usr/bin/pstruct
/usr/bin/ptar
/usr/bin/ptardiff
/usr/bin/ptargrep
/usr/bin/s2p
/usr/bin/shasum
/usr/bin/splain
/usr/bin/xsubpp
/usr/lib/libperl.so
%dir /usr/lib/perl5
%dir /usr/lib/perl5/%{version}
%dir /usr/lib/perl5/site_perl
%dir /usr/lib/perl5/site_perl/%{version}
%dir /usr/lib/perl5/site_perl/%{version}/%{_arch}-linux
%dir /usr/lib/perl5/site_perl/%{version}/%{_arch}-linux/auto
/usr/lib/perl5/%{version}/*
%exclude /usr/lib/perl5/%{version}/pod/*

%files extras
/usr/lib/perl5/%{version}/pod/*
/usr/share/man/man1/*.bz2
/usr/share/man/man3/*.bz2

%changelog
* Tue Jan 31 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 5.14.2-1
- Initial version
