Summary: cpio
Name: cpio
Version: 2.11
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/cpio
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 20fc912915c629e809f80b96b2e75d7d

%description
GNU cpio copies files into or out of a cpio or tar archive.
The archive can be another file on the disk, a magnetic tape, or a pipe.

%prep
%setup -q

%build
./configure --prefix=/usr --libexecdir=/usr/%{_lib}/cpio
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/cpio.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/cpio.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/cpio
/usr/%{_lib}/cpio
/usr/share/info/cpio.info
/usr/share/man/man1/cpio.1
/usr/share/man/man1/mt.1

%changelog
* Mon Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.11-1
- Initial version
