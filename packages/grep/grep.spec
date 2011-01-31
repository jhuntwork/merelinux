Summary: GNU Grep
Name: grep
Version: 2.7
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/grep
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = 9ea94cd8d9c8ca4d0ebe7c45ceeabf380907efcb
BuildRequires: pcre-devel

%description
%{name} searches one or more input files for lines
containing a match to a specified pattern.

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --bindir=/bin
make

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
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
/usr/share/man/man1/*.bz2

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7-1
- Upgrade to 2.7

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.3-1
- Upgrade to 2.6.3

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.6.1-1
- Upgrade to 2.6.1

* Sat Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.4-2
- Use FHS compatible info directories

* Tue Jul 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.5.4-1
- Initial version
