Summary: GNU Troff (Groff)
Name: groff
Version: 1.20.1
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/groff
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, gcc-libs, gcc-c++-libs
BuildRequires: digest(%{SOURCE0}) = 48fa768dd6fdeb7968041dd5ae8e2b02

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
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
PAGE=letter ./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}/groff
make

%install
make DESTDIR=%{buildroot} docdir=/usr/share/doc/%{name}-%{version} install
ln -sv eqn %{buildroot}/usr/bin/geqn
ln -sv tbl %{buildroot}/usr/bin/gtbl
rm -f %{buildroot}/usr/share/info/dir

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
/usr/share/man/man1/addftinfo.1
/usr/share/man/man1/afmtodit.1
/usr/share/man/man1/chem.1
/usr/share/man/man1/eqn.1
/usr/share/man/man1/eqn2graph.1
/usr/share/man/man1/gdiffmk.1
/usr/share/man/man1/grap2graph.1
/usr/share/man/man1/grn.1
/usr/share/man/man1/grodvi.1
/usr/share/man/man1/groff.1
/usr/share/man/man1/groffer.1
/usr/share/man/man1/grog.1
/usr/share/man/man1/grohtml.1
/usr/share/man/man1/grolbp.1
/usr/share/man/man1/grolj4.1
/usr/share/man/man1/grops.1
/usr/share/man/man1/grotty.1
/usr/share/man/man1/hpftodit.1
/usr/share/man/man1/indxbib.1
/usr/share/man/man1/lkbib.1
/usr/share/man/man1/lookbib.1
/usr/share/man/man1/mmroff.1
/usr/share/man/man1/neqn.1
/usr/share/man/man1/nroff.1
/usr/share/man/man1/pdfroff.1
/usr/share/man/man1/pfbtops.1
/usr/share/man/man1/pic.1
/usr/share/man/man1/pic2graph.1
/usr/share/man/man1/preconv.1
/usr/share/man/man1/refer.1
/usr/share/man/man1/roff2dvi.1
/usr/share/man/man1/roff2html.1
/usr/share/man/man1/roff2pdf.1
/usr/share/man/man1/roff2ps.1
/usr/share/man/man1/roff2text.1
/usr/share/man/man1/roff2x.1
/usr/share/man/man1/soelim.1
/usr/share/man/man1/tbl.1
/usr/share/man/man1/tfmtodit.1
/usr/share/man/man1/troff.1
/usr/share/man/man5/groff_font.5
/usr/share/man/man5/groff_out.5
/usr/share/man/man5/groff_tmac.5
/usr/share/man/man5/lj4_font.5
/usr/share/man/man7/ditroff.7
/usr/share/man/man7/groff.7
/usr/share/man/man7/groff_char.7
/usr/share/man/man7/groff_diff.7
/usr/share/man/man7/groff_hdtbl.7
/usr/share/man/man7/groff_man.7
/usr/share/man/man7/groff_mdoc.7
/usr/share/man/man7/groff_me.7
/usr/share/man/man7/groff_mm.7
/usr/share/man/man7/groff_mmse.7
/usr/share/man/man7/groff_mom.7
/usr/share/man/man7/groff_ms.7
/usr/share/man/man7/groff_trace.7
/usr/share/man/man7/groff_www.7
/usr/share/man/man7/roff.7

%files doc
%defattr(-,root,root)
/usr/share/doc/%{name}-%{version}

%changelog
* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.20.1-2
- Use FHS compatible info dirs. Use separate doc package.

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.20.1-1
- Initial version
