Summary: GNU Make
Name: make
Version: 3.81
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/make
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-upstream_fixes-1.patch

Requires: base-layout, glibc
Requires(post): texinfo, bash, ncurses, readline
BuildRequires: digest(%{SOURCE0}) = 354853e0b2da90c527e35aabb8d6f1e6
BuildRequires: digest(%{PATCH0}) = 8b1e478d8e733dc2d72e31bc7af1defa

%description
Make is a tool which controls the generation of executables and other
non-source files of a program from the program's source files.

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=/usr --infodir=/usr/share/info --mandir=/usr/share/man
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/make.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/make.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/make
/usr/share/info/make.info
/usr/share/info/make.info-1
/usr/share/info/make.info-2
/usr/share/man/man1/make.1

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.81-1
- Initial version
