Summary: GNU Ed - A line-oriented text editor
Name: ed
Version: 1.5
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/ed/ed.html
Source0: ftp://ftp.gnu.org/gnu/ed/ed-1.5.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = ab395cc58ad9c7464dd6dc3590be827aaf7aa680

%description
GNU ed is a line-oriented text editor. It is used to create, display, modify
and otherwise manipulate text files, both interactively and via shell scripts.
A restricted version of ed, red, can only edit files in the current directory
and cannot execute shell commands. Ed is the "standard" text editor in the
sense that it is the original editor for Unix, and thus widely available.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/ed.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/ed.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/ed
/usr/bin/red
/usr/share/info/ed.info
/usr/share/man/man1/ed.1.bz2
/usr/share/man/man1/red.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.5-1
- Initial version
