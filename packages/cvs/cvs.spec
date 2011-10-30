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
BuildRequires: vim
BuildRequires: zlib-devel

%description
CVS is a version control system, an important component of Source Configuration
Management (SCM). Using it, you can record the history of sources files, and
documents. It fills a similar role to the free software RCS, PRCS, and Aegis
packages.

%prep
%setup -q
%patch0 -p1
sed -i 's/getline /get_line /' lib/getline.{c,h}

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --with-editor=vi
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/cvs.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/cvsclient.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/cvs.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/cvsclient.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/cvs
/usr/bin/cvsbug
/usr/bin/rcs2log
/usr/share/cvs
/usr/share/info/cvs.info
/usr/share/info/cvs.info-1
/usr/share/info/cvs.info-2
/usr/share/info/cvsclient.info
/usr/share/man/man1/cvs.1.bz2
/usr/share/man/man5/cvs.5.bz2
/usr/share/man/man8/cvsbug.8.bz2

%changelog
* Sat Oct 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.11.23-1
- Initial version
