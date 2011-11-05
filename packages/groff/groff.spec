Summary: GNU Troff (Groff)
Name: groff
Version: 1.21
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/groff
Source0: http://ftp.gnu.org/gnu/groff/groff-1.21.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = a513aca4a7530a6e63325addd6ba2d282c8f1608

%package doc
Requires: %{name}
Summary: Documentation for %{name}

%description
The groff (GNU troff) software is a typesetting package which reads plain text
mixed with formatting commands and produces formatted output.

%description doc
Documentation for %{name}

%prep
%setup -q

%build
export CFLAGS="-Os -pipe"
export CXXFLAGS="-Os -pipe"
PAGE=letter ./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}/groff
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} docdir=/usr/share/doc/%{name}-%{version} install
ln -sv eqn %{buildroot}/usr/bin/geqn
ln -sv tbl %{buildroot}/usr/bin/gtbl
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/groff.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/groff.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/addftinfo
/usr/bin/afmtodit
/usr/bin/chem
/usr/bin/eqn
/usr/bin/eqn2graph
/usr/bin/gdiffmk
/usr/bin/geqn
/usr/bin/grap2graph
/usr/bin/grn
/usr/bin/grodvi
/usr/bin/groff
/usr/bin/groffer
/usr/bin/grog
/usr/bin/grolbp
/usr/bin/grolj4
/usr/bin/grops
/usr/bin/grotty
/usr/bin/gtbl
/usr/bin/hpftodit
/usr/bin/indxbib
/usr/bin/lkbib
/usr/bin/lookbib
/usr/bin/mmroff
/usr/bin/neqn
/usr/bin/nroff
/usr/bin/pdfroff
/usr/bin/pfbtops
/usr/bin/pic
/usr/bin/pic2graph
/usr/bin/post-grohtml
/usr/bin/pre-grohtml
/usr/bin/preconv
/usr/bin/refer
/usr/bin/roff2dvi
/usr/bin/roff2html
/usr/bin/roff2pdf
/usr/bin/roff2ps
/usr/bin/roff2text
/usr/bin/roff2x
/usr/bin/soelim
/usr/bin/tbl
/usr/bin/tfmtodit
/usr/bin/troff
/usr/%{_lib}/%{name}
/usr/share/%{name}
/usr/share/info/groff.info
/usr/share/info/groff.info-1
/usr/share/info/groff.info-2
/usr/share/info/groff.info-3
/usr/share/man/man1/*.bz2
/usr/share/man/man5/*.bz2
/usr/share/man/man7/*.bz2

%files doc
%defattr(-,root,root)
/usr/share/doc/%{name}-%{version}

%changelog
* Sat Nov 05 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.21-2
- Optimize for size

* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.21-1
- Upgrade to 1.21

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.20.1-2
- Use FHS compatible info dirs. Use separate doc package.

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.20.1-1
- Initial version
