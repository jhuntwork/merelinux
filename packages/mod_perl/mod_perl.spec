Summary: Apache Perl Module
Name: mod_perl
Version: 2.0.4
Release: 1
Group: Development/Languages
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://perl.apache.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 65299a16ec414a690a48a2bbe63acaa3c6bb897b
BuildRequires: httpd-devel
BuildRequires: apr-devel
BuildRequires: apr-util-devel
BuildRequires: expat-devel

%description
mod_perl brings together the full power of the Perl programming language and
the Apache HTTP server. You can use Perl to manage Apache, respond to requests
for web pages and much more.

%package devel
Summary: Headers and documentation for developing with mod_perl
Group: Development/Libraries
Requires: %{name}, httpd-devel

%description devel
Headers and documentation for developing with mod_perl

%prep
%setup -q
# we need to filter out a few auto requirements
cat > mod_perl-req << "EOF"
#!/bin/sh
%{__perl_requires} "$@" | sed \
        -e '/perl(Apache2::FunctionTable)/d' \
        -e '/perl(Apache2::StructureTable)/d' \
        -e '/perl(Apache::TestConfigParse)/d' \
	-e '/perl(Apache::TestConfigPerl)/d' \
	-e '/perl(BSD::Resource)/d' \
	-e '/perl(Data::Flow)/d'
EOF
chmod +x mod_perl-req
%define __perl_requires %{_builddir}/mod_perl-%{version}/mod_perl-req

%build
perl Makefile.PL MP_APXS=/usr/sbin/apxs
make

%install
make DESTDIR=%{buildroot} install
#find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -f %{buildroot}/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
find %{buildroot} -name ".packlist" -exec rm -vf '{}' \;

%clean
rm -rf %{buildroot}

%post
echo 'To activate this module, add the following lines to /etc/apache/httpd.conf:
LoadModule perl_module %{_lib}/apache/mod_perl.so'

%files
%defattr(-,root,root)
/usr/bin/mp2bug
/usr/%{_lib}/apache/mod_perl.so
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/APR.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/APR
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Apache
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Apache2
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/Apache2.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Bundle/ApacheTest.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/ModPerl
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/APR
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/Apache2
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/ModPerl
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/mod_perl2.pm

%files devel
%defattr(-,root,root)
/usr/include/apache/*
/usr/share/man/man3/*

%changelog
* Sat Sep 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.0.4-1
- Initial version
