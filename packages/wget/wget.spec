Summary: GNU Wget
Name: wget
Version: 1.12
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/wget
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, openssl
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 308a5476fc096a8a525d07279a6f6aa3
BuildRequires: openssl-devel

%description
GNU Wget is a free software package for retrieving files using HTTP, HTTPS
and FTP, the most widely-used Internet protocols. It is a non-interactive
commandline tool, so it may easily be called from scripts, cron jobs,
terminals without X-Windows support, etc.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --sysconfdir=/etc \
  --with-ssl
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/wget.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/wget.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/wget
/etc/wgetrc
/usr/share/info/wget.info
/usr/share/man/man1/wget.1

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.12-1
- Initial version
