Summary: GNU Tape Archiver
Name: tar
Version: 1.23
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/tar
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 41e2ca4b924ec7860e51b43ad06cdb7e

%description
The Tar program provides the ability to create tar archives,
as well as various other kinds of manipulation.

%prep
%setup -q

%build
sed -i /SIGPIPE/d src/tar.c
./configure --prefix=/usr --bindir=/bin --libexecdir=/usr/sbin
make
sed -i '35 i\
AT_UNPRIVILEGED_PREREQ' tests/remfiles01.at
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/tar.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/tar.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/tar
/usr/sbin/rmt
/usr/share/info/tar.info
/usr/share/info/tar.info-1
/usr/share/info/tar.info-2

%changelog
* Tue Apr 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.23-1
- Initial version
