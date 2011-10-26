Summary: The GNU Documentation System
Name: texinfo
Version: 4.13a
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/texinfo
Source0: http://ftp.gnu.org/gnu/texinfo/texinfo-4.13a.tar.lzma

BuildRequires: digest(sha1:%{SOURCE0}) = 676ec9aa25a97c05dff66fba5225f9e101160063
BuildRequires: ncurses-devel

%package tex
Summary: Tools for formatting texinfo docs for printing using TeX.
Group: Applications/Publishing
Requires: %{name} = %{version}-%{release}

%description
%{name} is the official documentation format of the GNU project and is used by many
other projects as well.

%description tex
Tools for formatting texinfo docs for printing using TeX.

%prep
%setup -q -n %{name}-4.13

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=/usr/share/texmf install-tex
%{compress_man}
%{strip}
%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/info
/usr/bin/infokey
/usr/bin/install-info
/usr/bin/makeinfo
/usr/bin/pdftexi2dvi
/usr/bin/texi2dvi
/usr/bin/texi2pdf
/usr/bin/texindex
/usr/share/info/dir
/usr/share/info/info-stnd.info
/usr/share/info/info.info
/usr/share/info/texinfo
/usr/share/info/texinfo-1
/usr/share/info/texinfo-2
/usr/share/info/texinfo-3
/usr/share/man/man1/info.1.bz2
/usr/share/man/man1/infokey.1.bz2
/usr/share/man/man1/install-info.1.bz2
/usr/share/man/man1/makeinfo.1.bz2
/usr/share/man/man1/pdftexi2dvi.1.bz2
/usr/share/man/man1/texi2dvi.1.bz2
/usr/share/man/man1/texi2pdf.1.bz2
/usr/share/man/man1/texindex.1.bz2
/usr/share/man/man5/info.5.bz2
/usr/share/man/man5/texinfo.5.bz2
/usr/share/texinfo

%files tex
%defattr(-,root,root)
/usr/share/texmf

%changelog
* Tue Oct 25 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.13a-3
- Optimize for size

* Sat Jul 17 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.13a-2
- Add Build requirement for ncurses-devel

* Tue Aug 04 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
