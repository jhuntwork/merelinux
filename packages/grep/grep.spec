Summary: GNU Grep
Name: grep
Version: 2.9
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/grep
Source0: http://ftp.gnu.org/gnu/grep/grep-2.9.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = 0395eddfbf23e8ef1475677fce7c19a631abea41
BuildRequires: pcre-devel

%description
%{name} searches one or more input files for lines
containing a match to a specified pattern.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --bindir=/bin
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}
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
* Sat Nov 05 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.9-1
- Upgrade to 2.9
- Optimize for size

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
