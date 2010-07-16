Summary: GNU Bash
Name: bash
Version: 4.1
Release: 4
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/bash
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-rpm_requires-1.patch
Patch1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-upstream_fixes_1-5.patch

Requires: glibc, ncurses, readline

BuildRequires: digest(%{SOURCE0}) = 9800d8724815fd84994d9be65ab5e7b8
BuildRequires: digest(%{PATCH0}) = 98b964e1d400a2e301e7cdb34019e599
BuildRequires: digest(%{PATCH1}) = df1aab878fcb3b7955e15f8e5444c037
BuildRequires: readline-devel

%package doc
Summary: Bash Documentation 
Requires: texinfo, bash

%description
Bash is an sh-compatible shell that incorporates useful features from the
Korn shell (ksh) and C shell (csh).

%description doc
Extensive documentation for the GNU Bash shell

%prep
%setup -q
%patch0 -p1
%patch1 -p1

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
install -dv %{buildroot}/etc
cat > %{buildroot}/etc/bashrc << "EOF"
alias ls='ls --color=auto'
alias ll='ls -l'
eval $(dircolors -b /etc/dircolors)

# Setup a red prompt for root and a green one for users. 
NORMAL="\[\e[0m\]"
RED="\[\e[1;31m\]"
GREEN="\[\e[1;32m\]"
if [[ $EUID == 0 ]] ; then
        PS1="$RED\u$NORMAL@\h $RED[ $NORMAL\w$RED ]# $NORMAL"
else
        PS1="$GREEN\u$NORMAL@\h $GREEN[ $NORMAL\w$GREEN ]\$ $NORMAL"
fi

if [ "`locale charmap 2>/dev/null`" = "UTF-8" ]
then
	stty iutf8
fi
EOF
cat > %{buildroot}/etc/profile << "EOF"
export PATH=/bin:/usr/bin:/sbin:/usr/sbin
export INPUTRC=/etc/inputrc
export PKG_CONFIG_PATH="/usr/%{_lib}/pkgconfig"
source /etc/bashrc
EOF
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
/etc/bashrc
/etc/profile
/usr/share/man/man1/bash.1
/usr/share/man/man1/bashbug.1

%files doc
/usr/share/doc/%{name}-%{version}
/usr/share/info/bash.info

%changelog
* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-4
- Updated bash rpm-requires patch

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-3
- Add in user environment files, fix build dependencies

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-2
- Add in upstream patches

* Tue Mar 30 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.1-1
- Uppdated to 4.1

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-3
- Use FHS compatible info directories

* Thu Sep 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-2
- Updated upstream patches

* Thu Aug 13 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0-1
- Initial version
