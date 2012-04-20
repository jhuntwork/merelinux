Summary: cvs
Name: cvs
Version: 1.11.23
Release: 1
Group: Development/Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://savannah.nongnu.org/projects/cvs
Source0: http://ftp.gnu.org/non-gnu/cvs/source/stable/1.11.23/cvs-1.11.23.tar.bz2
Patch0: http://www.linuxfromscratch.org/patches/blfs/svn/cvs-1.11.23-zlib-1.patch

BuildRequires: digest(sha1:%{SOURCE0}) = a51c531eebaff2dfdcc0fb6d94c8c6e509e06d7d
BuildRequires: digest(sha1:%{PATCH0})  = 0d20bab8a6b6e419a8c900d082b487ad6a3aec38
BuildRequires: zlib-devel

%description
CVS is a version control system, an important component of Source Configuration
Management (SCM). Using it, you can record the history of sources files, and
documents. It fills a similar role to the free software RCS, PRCS, and Aegis
packages.

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q
%patch0 -p1
sed -i 's/getline /get_line /' lib/getline.c lib/getline.h

%build
export CFLAGS='-D_GNU_SOURCE -Os -pipe'
export LDFLAGS='--static'
./configure \
  --prefix='' \
  --with-editor=vi
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -rf %{buildroot}/share/info
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/cvs
/share/man/man1/cvs.1.bz2
/share/man/man5/cvs.5.bz2

%files extras
%defattr(-,root,root)
/bin/cvsbug
/bin/rcs2log
/share/cvs
/share/man/man8/cvsbug.8.bz2

%changelog
* Thu Apr 19 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.11.23-1
- Initial version
