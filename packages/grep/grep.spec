Summary: GNU Grep
Name: grep
Version: 2.6.3
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/grep
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, pcre
BuildRequires: digest(%{SOURCE0}) = 3095b57837b312f087c0680559de7f13
BuildRequires: pcre-devel

%description
%{name} searches one or more input files for lines
containing a match to a specified pattern.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --bindir=/bin
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/grep.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/grep.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/bin/egrep
/bin/fgrep
/bin/grep
/usr/share/info/grep.info
/usr/share/man/man1/egrep.1
/usr/share/man/man1/fgrep.1
/usr/share/man/man1/grep.1

%changelog
* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.3-1
- Upgrade to 2.6.3

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-1
- Upgrade to 2.6.1

* Sat Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.4-2
- Use FHS compatible info directories

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.4-1
- Initial version
