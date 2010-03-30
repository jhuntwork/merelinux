Summary: Perl Progamming Language
Name: perl
Version: 5.10.1
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.perl.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, zlib
BuildRequires: digest(%{SOURCE0}) = 82400c6d34f7b7b43d0196c76cd2bbb1

Provides: perl, perl(Carp::Heavy), perl(getopts.pl)

%description
Perl is a stable, cross platform programming language.

%prep
%setup -q
# perl doesn't conform to POSIX sh and doesn't offer any easy workaround
mkdir bin
ln -s /bin/bash bin/sh

# fix CGI scripts
sed -i 's@/usr/local/bin/perl@%{_bindir}/perl@' lib/CGI/eg/*

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
       -e "s|LIB\s*= ./zlib-src|LIB = /usr/%{_lib}|" \
       ext/Compress-Raw-Zlib/config.in
sh Configure -des -Dprefix=/usr \
                  -Dvendorprefix=/usr           \
                  -Dman1dir=/usr/share/man/man1 \
                  -Dman3dir=/usr/share/man/man3 \
                  -Dpager="/usr/bin/less -isR"
make
#make test

%install
make DESTDIR=%{buildroot} install

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
/usr/bin/s2p
/usr/bin/shasum
/usr/bin/splain
/usr/bin/xsubpp
/usr/lib/perl5
/usr/share/man/man1/*
/usr/share/man/man3/*

%changelog
* Sat Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Upgrade to 5.10.1

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
