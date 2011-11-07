Summary: GNU Coreutils
Name: coreutils
Version: 8.14
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/coreutils
Source0: ftp://ftp.gnu.org/gnu/coreutils/coreutils-8.14.tar.xz

BuildRequires: digest(sha1:%{SOURCE0}) = cda40d00ea68486c33a31a3bfb7c80dd2cd2e9d6
BuildRequires: shadow

%description
A collection of core system utilities, such as cp, mv, ls

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --enable-no-install-program=kill,uptime \
  --libdir=/usr/%{_lib} \
  --libexecdir=/usr/%{_lib}/coreutils
make %{PMFLAGS}
#make NON_ROOT_USERNAME=nobody check-root
#chown -R nobody .
#echo "dummy:x:1000:nobody" >> /etc/group
#su nobody -s /bin/bash -c "make RUN_EXPENSIVE_TESTS=yes check"

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}
mkdir -v %{buildroot}/bin
mkdir -v %{buildroot}/usr/sbin
for file in cat chgrp chmod chown cp date dd df dirname echo false head ln ls mkdir mknod mv nice pwd readlink rm rmdir sleep stty sync touch true uname
do
  mv -v %{buildroot}/usr/bin/$file %{buildroot}/bin
done
mv -v %{buildroot}/usr/bin/chroot %{buildroot}/usr/sbin
rm -f %{buildroot}/usr/share/info/dir
install -dv %{buildroot}/etc
%{buildroot}/usr/bin/dircolors -p > %{buildroot}/etc/dircolors
%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/coreutils.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/coreutils.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/bin/cat
/bin/chgrp
/bin/chmod
/bin/chown
/bin/cp
/bin/date
/bin/dd
/bin/df
/bin/dirname
/bin/echo
/bin/false
/bin/head
/bin/ln
/bin/ls
/bin/mkdir
/bin/mknod
/bin/mv
/bin/nice
/bin/pwd
/bin/readlink
/bin/rm
/bin/rmdir
/bin/sleep
/bin/stty
/bin/sync
/bin/touch
/bin/true
/bin/uname
/etc/dircolors
/usr/bin/[
/usr/bin/base64
/usr/bin/basename
/usr/bin/chcon
/usr/bin/cksum
/usr/bin/comm
/usr/bin/csplit
/usr/bin/cut
/usr/bin/dir
/usr/bin/dircolors
/usr/bin/du
/usr/bin/env
/usr/bin/expand
/usr/bin/expr
/usr/bin/factor
/usr/bin/fmt
/usr/bin/fold
/usr/bin/groups
/usr/bin/hostid
/usr/bin/id
/usr/bin/install
/usr/bin/join
/usr/bin/link
/usr/bin/logname
/usr/bin/md5sum
/usr/bin/mkfifo
/usr/bin/mktemp
/usr/bin/nl
/usr/bin/nohup
/usr/bin/nproc
/usr/bin/od
/usr/bin/paste
/usr/bin/pathchk
/usr/bin/pinky
/usr/bin/pr
/usr/bin/printenv
/usr/bin/printf
/usr/bin/ptx
/usr/bin/runcon
/usr/bin/seq
/usr/bin/sha1sum
/usr/bin/sha224sum
/usr/bin/sha256sum
/usr/bin/sha384sum
/usr/bin/sha512sum
/usr/bin/shred
/usr/bin/shuf
/usr/bin/sort
/usr/bin/split
/usr/bin/stat
/usr/bin/stdbuf
/usr/bin/sum
/usr/bin/tac
/usr/bin/tail
/usr/bin/tee
/usr/bin/test
/usr/bin/timeout
/usr/bin/tr
/usr/bin/truncate
/usr/bin/tsort
/usr/bin/tty
/usr/bin/unexpand
/usr/bin/uniq
/usr/bin/unlink
/usr/bin/users
/usr/bin/vdir
/usr/bin/wc
/usr/bin/who
/usr/bin/whoami
/usr/bin/yes
/usr/%{_lib}/coreutils
/usr/sbin/chroot
/usr/share/info/coreutils.info
/usr/share/man/man1/*.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.14-1
- Upgrade to 8.14
- Optimize from size

* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.12-1
- Upgrade to 8.12

* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.9-1
- Upgrade to 8.9

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.5-1
- Upgrade to 8.5

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.4-2
- Add in dependency on gmp, create a dircolors listing

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.4-1
- Upgrade to 8.4

* Mon Dec 28 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 8.2-1
- Upgrade to 8.2

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.6-2
- Use FHS compatible info directories

* Mon Oct 24 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.6-1
- Upgrade to 7.6

* Mon Jul 27 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.4-1
- Initial version
