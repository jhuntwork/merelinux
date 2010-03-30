Summary: GNU Bash
Name: bash
Version: 4.1
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bash
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-rpm_requires-1.patch

Requires: glibc, ncurses, readline

BuildRequires: digest(%{SOURCE0}) = 9800d8724815fd84994d9be65ab5e7b8
BuildRequires: digest(%{PATCH0}) = 7b9ef6862dc12cb3489ebb0d0e7801e6

%package doc
Summary: Bash Documentation 

%description
%{name} is an sh-compatible shell that incorporates useful features from the
Korn shell (ksh) and C shell (csh).

%description doc
Extensive documentation for the GNU Bash shell

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=/usr --bindir=/bin --without-bash-malloc \
  --htmldir=/usr/share/doc/%{name}-%{version}  --with-installed-readline
make
#sed -i 's/LANG/LC_ALL/' tests/intl.tests
#sed -i 's@tests@& </dev/tty@' tests/run-test
#chown -Rv nobody ./
#su nobody -s /bin/bash -c "make tests"

%install
make DESTDIR=%{buildroot} install
ln -vs bash %{buildroot}/bin/sh
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post doc
/usr/bin/install-info /usr/share/info/bash.info /usr/share/info/dir

%preun doc
/usr/bin/install-info --delete /usr/share/info/bash.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/bin/bash
/bin/bashbug
/bin/sh
/usr/share/man/man1/bash.1
/usr/share/man/man1/bashbug.1

%files doc
/usr/share/doc/%{name}-%{version}
/usr/share/info/bash.info

%changelog
* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-1
- Uppdated to 4.1

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-3
- Use FHS compatible info directories

* Thu Sep 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-2
- Updated upstream patches

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-1
- Initial version
