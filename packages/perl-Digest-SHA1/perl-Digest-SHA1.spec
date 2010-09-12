Summary: perl interface to the SHA1 algorithm
Name: perl-Digest-SHA1
Version: 2.13
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://search.cpan.org/~gaas/Digest-SHA1-%{version}
Source0: http://dev.lightcube.us/sources/perl-modules/Digest-SHA1-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 77379a2775c744dd7a9890f5638da6362ae58013

%description
The perl interface to the SHA1 algorithm

%prep
%setup -q -n Digest-SHA1-%{version}

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
perl Makefile.PL
make
make test

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
rm -f %{buildroot}/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
find %{buildroot} -name ".packlist" -exec rm -vf '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/Digest
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/Digest
/usr/share/man/man3/*

%changelog
* Sat Sep 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.13-1
- Initial version
