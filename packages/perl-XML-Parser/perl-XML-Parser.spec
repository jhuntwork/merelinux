Summary: perl XML Parser
Name: perl-XML-Parser
Version: 2.36
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://search.cpan.org/~msergeant
Source0: http://dev.lightcube.us/sources/perl-modules/XML-Parser-%{version}.tar.gz

BuildRequires: digest(%{SOURCE0}) = 1b868962b658bd87e1563ecd56498ded

%description
A perl module for parsing XML documents

%prep
%setup -q -n XML-Parser-%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
perl Makefile.PL
make
make test

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/XML
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto
/usr/share/man/man3/XML::Parser::Expat.3.bz2
/usr/share/man/man3/XML::Parser.3.bz2
/usr/share/man/man3/XML::Parser::Style::Debug.3.bz2
/usr/share/man/man3/XML::Parser::Style::Objects.3.bz2
/usr/share/man/man3/XML::Parser::Style::Stream.3.bz2
/usr/share/man/man3/XML::Parser::Style::Subs.3.bz2
/usr/share/man/man3/XML::Parser::Style::Tree.3.bz2

%changelog
* Wed Aug 25 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.36-1
- Initial version
