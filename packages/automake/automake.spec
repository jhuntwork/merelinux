Summary: GNU Automake
Name: automake
Version: 1.11.1
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.gnu.org/software/automake
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, bash, automake
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = c2972c4d9b3e29c03d5f2af86249876f

%description
Automake is a tool for automatically generating `Makefile.in' files compliant
with the GNU Coding Standards.

%prep
%setup -q

%build
./configure --prefix=/usr
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/automake.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/automake.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/aclocal
/usr/bin/aclocal-1.11
/usr/bin/automake
/usr/bin/automake-1.11
/usr/share/aclocal-1.11
/usr/share/automake-1.11
/usr/share/doc/automake
/usr/share/info/automake.info
/usr/share/info/automake.info-1
/usr/share/info/automake.info-2
/usr/share/man/man1/aclocal-1.11.1
/usr/share/man/man1/aclocal.1
/usr/share/man/man1/automake-1.11.1
/usr/share/man/man1/automake.1

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.11.1-1
- Initial version
