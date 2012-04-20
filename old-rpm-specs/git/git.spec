Summary: git
Name: git
Version: 1.7.2.2
Release: 2
Group: Development/Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://git-scm.com
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 0cc1caba421a2af5f8e3b9648a6230ea07c60bee
BuildRequires: openssl-devel
BuildRequires: expat-devel
BuildRequires: zlib-devel
BuildRequires: curl-devel

%description
Git is a free & open source, distributed version control system designed to
handle everything from small to very large projects with speed and
efficiency.

%package svn
Summary: Utility to convert subversion repositories to git
Group: Development/Utilities
Requires: %{name}

%description svn
Utility to convert subversion repositories to git

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/lib \
  --with-zlib \
  --with-pager=/usr/bin/less \
  --with-editor=/usr/bin/vim \
  --with-shell=/bin/bash \
  --with-perl=/usr/bin/perl \
  --with-python=/usr/bin/python
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;
# Remove git-cvsserver, we don't want the dependencies that go with it
rm -v %{buildroot}/usr/{bin,lib/git-core}/git-cvsserver
rm -v %{buildroot}/usr/lib/perl5/5.12.1/%{_arch}-linux/perllocal.pod
find %{buildroot}/usr/lib/git-core/ -mindepth 1 -not -name "git-svn" | sed 's@%{buildroot}@@' > git-core-files

%clean
rm -rf %{buildroot}

%files -f git-core-files
%defattr(-,root,root)
/usr/bin/git
/usr/bin/git-receive-pack
/usr/bin/git-shell
/usr/bin/git-upload-archive
/usr/bin/git-upload-pack
/usr/bin/gitk
%dir /usr/lib/git-core
/usr/share/git-core
/usr/share/git-gui
/usr/share/gitk
/usr/share/gitweb
/usr/share/man/man3/Git.3.bz2
/usr/share/man/man3/private-Error.3.bz2
/usr/lib/perl5/site_perl/5.12.1/Error.pm
/usr/lib/perl5/site_perl/5.12.1/Git.pm
/usr/lib/perl5/site_perl/5.12.1/%{_arch}-linux/auto/Git
/usr/lib/python2.7/site-packages/git_remote_helpers-0.1.0-py2.7.egg-info
/usr/lib/python2.7/site-packages/git_remote_helpers

%files svn
%defattr(-,root,root)
/usr/lib/git-core/git-svn

%changelog
* Wed Sep 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.2.2-2
- Add in support for git-svn

* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.2.2-1
- Initial version
