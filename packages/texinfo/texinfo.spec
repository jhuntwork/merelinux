Summary: The GNU Documentation System
Name: texinfo
Version: 4.13a
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/texinfo
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, ncurses, bash
BuildRequires: digest(%{SOURCE0}) = 71ba711519209b5fb583fed2b3d86fcb

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
./configure --prefix=/usr
make
make check

%install
make DESTDIR=%{buildroot} install
make DESTDIR=%{buildroot} TEXMF=/usr/share/texmf install-tex
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
/usr/share/man/man1/info.1
/usr/share/man/man1/infokey.1
/usr/share/man/man1/install-info.1
/usr/share/man/man1/makeinfo.1
/usr/share/man/man1/pdftexi2dvi.1
/usr/share/man/man1/texi2dvi.1
/usr/share/man/man1/texi2pdf.1
/usr/share/man/man1/texindex.1
/usr/share/man/man5/info.5
/usr/share/man/man5/texinfo.5
/usr/share/texinfo

%files tex
%defattr(-,root,root)
/usr/share/texmf/*

%changelog
* Tue Aug 4 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> -
- Initial version
