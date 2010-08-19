Summary: GNU Which
Name: which
Version: 2.20
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.xs4all.nl/~carlo17/which
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 95be0501a466e515422cde4af46b2744

%description
Which is a utility that prints out the full path of the executables that
bash(1) would execute when the passed program names would have been entered
on the shell prompt. It does this by using the exact same algorithm as bash.
Tildes and a dot in the PATH are now expanded to the full path by default.
Options allow to rather print "~/*" or "./*" and/or to print all exectuables
that match any directory in PATH.

%prep
%setup -q

%build
./configure \
  --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%post
/usr/bin/install-info /usr/share/info/which.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/which.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/which
/usr/share/info/which.info
/usr/share/man/man1/which.1

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.20-1
- Initial version
