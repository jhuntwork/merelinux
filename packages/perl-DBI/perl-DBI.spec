Summary: perl DBI module
Name: perl-DBI
Version: 1.613
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://dbi.perl.org
Source0: http://dev.lightcube.us/sources/perl-modules/DBI-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = 1fb75474c3ff75fcbc16a98656e8f89d

%description
The DBI is the standard database interface module for Perl. It defines a set of
methods, variables and conventions that provide a consistent database interface
independent of the actual database being used.

%prep
%setup -q -n DBI-%{version}
cat > %{name}-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed \
  -e '/perl(RPC::PlClient)/d' \
  -e '/perl(RPC::PlServer)/d' \
  -e '/perl(Win32::ODBC)/d'
EOF
chmod +x %{name}-req
%define __perl_requires %{_builddir}/DBI-%{version}/%{name}-req

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
perl Makefile.PL
make
#make test

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -f %{buildroot}/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
install -dv %{buildroot}/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/DBD
install -dv %{buildroot}/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/DBD 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/dbiprof
/usr/bin/dbilogstrip
/usr/bin/dbiproxy
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/DBI.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/DBD
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/DBI.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/DBI
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Roadmap.pod
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/TASKS.pod
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Win32
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/DBI
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/dbixs_rev.pl
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/DBD
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/DBD
/usr/share/man/man1/*
/usr/share/man/man3/*

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.613-1
- Initial version
