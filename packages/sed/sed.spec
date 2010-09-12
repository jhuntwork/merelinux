Summary: GNU Streams Editor
Name: sed
Version: 4.2.1
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/sed
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 7d310fbd76e01a01115075c1fd3f455a

%description
Sed is used to filter text and perform modifications on it.

%prep
%setup -q

%build
./configure --prefix=/usr --bindir=/bin
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/sed.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/sed.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/sed
/usr/share/info/sed.info
/usr/share/man/man1/sed.1

%changelog
* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-2
- Use FHS compatible info directories

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-1
- Initial version
