Summary: git
Name: git
Version: 1.7.2.2
Release: 1
Group: Services
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://git-scm.com
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(%{SOURCE0}) = 4a5840b6d650692cb320eddb5ccefbaf
BuildRequires: openssl-devel
BuildRequires: expat-devel
BuildRequires: zlib-devel
BuildRequires: curl-devel

%description
Git is a free & open source, distributed version control system designed to
handle everything from small to very large projects with speed and
efficiency.

%prep
%setup -q

%build
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/lib
make

%install
make DESTDIR=%{buildroot} install
# Remove git-svn and git-cvsserver, we don't want the dependencies that go with it
rm -v %{buildroot}/usr/{bin,lib/git-core}/git-cvsserver
rm -v %{buildroot}/usr/lib/git-core/git-svn

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/git
/usr/bin/git-receive-pack
/usr/bin/git-shell
/usr/bin/git-upload-archive
/usr/bin/git-upload-pack
/usr/bin/gitk
/usr/lib/git-core
/usr/share/git-core
/usr/share/git-gui
/usr/share/gitk
/usr/share/gitweb
/usr/share/man/man3/Git.3
/usr/share/man/man3/private-Error.3
/usr/lib/perl5/5.12.1/x86_64-linux/perllocal.pod
/usr/lib/perl5/site_perl/5.12.1/Error.pm
/usr/lib/perl5/site_perl/5.12.1/Git.pm
/usr/lib/perl5/site_perl/5.12.1/x86_64-linux/auto/Git
/usr/lib/python2.7/site-packages/git_remote_helpers-0.1.0-py2.7.egg-info
/usr/lib/python2.7/site-packages/git_remote_helpers

%changelog
* Mon Aug 23 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.7.2.2-1
- Initial version
