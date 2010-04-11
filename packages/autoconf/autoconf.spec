Summary: GNU Autoconf
Name: autoconf
Version: 2.65
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://www.gnu.org/software/autoconf
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, bash, m4
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = a6de1cc6434cd64038b0a0ae4e252b33

%description
Autoconf is an extensible package of M4 macros that produce
shell scripts to automatically configure software source code packages.

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
/usr/bin/install-info /usr/share/info/autoconf.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/standards.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/autoconf.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/standards.info /usr/share/info/dir

%files
%defattr(-,root,root)
/usr/bin/autoconf
/usr/bin/autoheader
/usr/bin/autom4te
/usr/bin/autoreconf
/usr/bin/autoscan
/usr/bin/autoupdate
/usr/bin/ifnames
/usr/share/autoconf
/usr/share/info/autoconf.info
/usr/share/info/standards.info
/usr/share/man/man1/autoconf.1
/usr/share/man/man1/autoheader.1
/usr/share/man/man1/autom4te.1
/usr/share/man/man1/autoreconf.1
/usr/share/man/man1/autoscan.1
/usr/share/man/man1/autoupdate.1
/usr/share/man/man1/config.guess.1
/usr/share/man/man1/config.sub.1
/usr/share/man/man1/ifnames.1


%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.65-1
- Initial version
