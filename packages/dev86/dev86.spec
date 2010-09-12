Summary: Dev86 
Name: dev86
Version: 0.16.17
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://homepage.ntlworld.com/robert.debath/dev86
Source0: http://dev.lightcube.us/sources/%{name}/Dev86src-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 0bfe55c7a5e11d72f19f26cb0383178605951c72

%description

%prep
%setup -q

%build
#sed -i -e 's@alt-libs elksemu@alt-libs@' \
#       -e 's@install-lib install-emu@install-lib@' \
#    makefile.in
make MANDIR=/usr/share/man

%install
make DIST=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/ar86
/usr/bin/as86
/usr/bin/bcc
/usr/bin/elksemu
/usr/bin/ld86
/usr/bin/nm86
/usr/bin/objdump86
/usr/bin/size86
/usr/lib/bcc
/usr/share/man/man1/as86.1.bz2
/usr/share/man/man1/bcc.1.bz2
/usr/share/man/man1/elks.1.bz2
/usr/share/man/man1/elksemu.1.bz2
/usr/share/man/man1/ld86.1.bz2

%changelog
* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.16.17-1
- Initial version
