Summary: perl mysql driver
Name: perl-DBD-mysql
Version: 4.017
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://dbi.perl.org
Source0: http://dev.lightcube.us/sources/perl-modules/DBD-mysql-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = e150b530806fb6a6c5dc75ac82cdd252adfb8055
BuildRequires: perl-DBI
BuildRequires: mysql-devel
BuildRequires: openssl-devel
BuildRequires: zlib-devel

%description
MySQL driver for the Perl5 Database Interface (DBI)

%prep
%setup -q -n DBD-mysql-%{version}

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

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/DBD/mysql.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/DBD/mysql.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/DBD/mysql
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/DBD/mysql
/usr/share/man/man3/*

%changelog
* Sat Sep 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.017-1
- Initial version
