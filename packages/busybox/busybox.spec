Summary: BusyBox: The Swiss Army Knife of Embedded Linux
Name: busybox
Version: 1.19.4
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://busybox.net
Source0: http://busybox.net/downloads/busybox-%{version}.tar.bz2
Source1: busybox-config

BuildRequires: digest(sha1:%{SOURCE0}) = 5d7db83d8efbadc19c86ec236e673504bbf43517
BuildRequires: digest(sha1:%{SOURCE1}) = b2f7857dbd6c5199401656d4ce37afe5bd46ff4c

%description
BusyBox combines tiny versions of many common UNIX utilities into a single small
executable. It provides replacements for most of the utilities you usually find
in GNU fileutils, shellutils, etc. The utilities in BusyBox generally have fewer
options than their full-featured GNU cousins; however, the options that are
included provide the expected functionality and behave very much like their GNU
counterparts. BusyBox provides a fairly complete environment for any small or
embedded system.

%prep
%setup -q
sed -i '/netinet\/ether/d' networking/arp.c
sed -i '/net\/if_slip/d' networking/ifconfig.c
sed -i '/net\/if_packet/d' networking/libiproute/iplink.c
sed -i '/getpwent/s@!.*@(pwent = getpwent()) != NULL) {@' loginutils/deluser.c
sed -i -e '/struct passwd \*pw/d' \
  -e 's@struct passwd pwent@struct passwd \*pwent@' \
  -e 's@pwent\.pw@pwent->pw@g' loginutils/deluser.c
sed '/CONFIG_PREFIX/s@=.*@="%{buildroot}/"@' %{SOURCE1} >.config

%build
export CFLAGS="-Os -Werror=implicit-function-declaration"
make V=1 HOSTCC="gcc -D_GNU_SOURCE" %{PMFLAGS}

%install
make V=1 HOSTCC="gcc -D_GNU_SOURCE" install
chmod u+s %{buildroot}/bin/busybox
install -d %{buildroot}/bin
install -d %{buildroot}/sbin
rm -f %{buildroot}/bin/ip
ln -s ../bin/busybox %{buildroot}/sbin/ip
# We want the bash capability but don't want to 'own' the /bin/bash file
rm -f %{buildroot}/bin/bash
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/[
/bin/[[
/bin/add-shell
/bin/addgroup
/bin/adduser
/bin/ash
/bin/awk
/bin/base64
/bin/basename
/bin/beep
/bin/bunzip2
/bin/busybox
/bin/bzcat
/bin/bzip2
/bin/cal
/bin/cat
/bin/catv
/bin/chgrp
/bin/chmod
/bin/chown
/bin/chvt
/bin/cksum
/bin/clear
/bin/cmp
/bin/comm
/bin/cp
/bin/cryptpw
/bin/cut
/bin/date
/bin/dc
/bin/dd
/bin/deallocvt
/bin/delgroup
/bin/deluser
/bin/df
/bin/diff
/bin/dirname
/bin/dmesg
/bin/dnsdomainname
/bin/dos2unix
/bin/du
/bin/dumpkmap
/bin/echo
/bin/ed
/bin/egrep
/bin/env
/bin/expand
/bin/expr
/bin/false
/bin/fdflush
/bin/fdformat
/bin/fgconsole
/bin/fgrep
/bin/find
/bin/flock
/bin/fold
/bin/free
/bin/fsync
/bin/ftpget
/bin/ftpput
/bin/fuser
/bin/getopt
/bin/grep
/bin/groups
/bin/gunzip
/bin/gzip
/bin/hd
/bin/head
/bin/hexdump
/bin/hostid
/bin/hostname
/bin/hush
/bin/id
/bin/install
/bin/ionice
/bin/iostat
/bin/ipaddr
/bin/ipcalc
/bin/ipcrm
/bin/ipcs
/bin/iplink
/bin/iproute
/bin/iprule
/bin/iptunnel
/bin/kbd_mode
/bin/kill
/bin/killall
/bin/killall5
/bin/last
/bin/less
/bin/ln
/bin/logger
/bin/login
/bin/logname
/bin/ls
/bin/lspci
/bin/lsusb
/bin/lzcat
/bin/lzma
/bin/lzop
/bin/lzopcat
/bin/makemime
/bin/md5sum
/bin/mesg
/bin/microcom
/bin/mkdir
/bin/mkfifo
/bin/mknod
/bin/mkpasswd
/bin/mktemp
/bin/more
/bin/mount
/bin/mountpoint
/bin/mpstat
/bin/mv
/bin/nc
/bin/netstat
/bin/nice
/bin/nmeter
/bin/nohup
/bin/nslookup
/bin/od
/bin/openvt
/bin/passwd
/bin/pgrep
/bin/pidof
/bin/ping
/bin/ping6
/bin/pipe_progress
/bin/pkill
/bin/pmap
/bin/powertop
/bin/printenv
/bin/printf
/bin/ps
/bin/pstree
/bin/pwd
/bin/pwdx
/bin/readlink
/bin/realpath
/bin/reformime
/bin/remove-shell
/bin/renice
/bin/reset
/bin/resize
/bin/rev
/bin/rm
/bin/rmdir
/bin/rpm2cpio
/bin/rtcwake
/bin/rx
/bin/script
/bin/scriptreplay
/bin/sed
/bin/seq
/bin/setkeycodes
/bin/setserial
/bin/setsid
/bin/sh
/bin/sha1sum
/bin/sha256sum
/bin/sha512sum
/bin/showkey
/bin/sleep
/bin/smemcap
/bin/sort
/bin/split
/bin/stat
/bin/strings
/bin/stty
/bin/su
/bin/sum
/bin/sync
/bin/tac
/bin/tail
/bin/tar
/bin/tee
/bin/telnet
/bin/test
/bin/time
/bin/timeout
/bin/top
/bin/touch
/bin/tr
/bin/traceroute
/bin/traceroute6
/bin/true
/bin/tty
/bin/ttysize
/bin/umount
/bin/uname
/bin/unexpand
/bin/uniq
/bin/unix2dos
/bin/unlzma
/bin/unlzop
/bin/unxz
/bin/unzip
/bin/uptime
/bin/users
/bin/usleep
/bin/uudecode
/bin/uuencode
/bin/vi
/bin/vlock
/bin/volname
/bin/wall
/bin/watch
/bin/wc
/bin/which
/bin/who
/bin/whoami
/bin/whois
/bin/xargs
/bin/xz
/bin/xzcat
/bin/yes
/bin/zcat
/sbin/acpid
/sbin/adjtimex
/sbin/arp
/sbin/blkid
/sbin/blockdev
/sbin/brctl
/sbin/chpasswd
/sbin/chroot
/sbin/devmem
/sbin/dnsd
/sbin/fbset
/sbin/fbsplash
/sbin/fdisk
/sbin/findfs
/sbin/freeramdisk
/sbin/fsck
/sbin/getty
/sbin/halt
/sbin/hdparm
/sbin/hwclock
/sbin/ifconfig
/sbin/init
/sbin/inotifyd
/sbin/ip
/sbin/klogd
/sbin/loadfont
/sbin/loadkmap
/sbin/logread
/sbin/losetup
/sbin/makedevs
/sbin/man
/sbin/mdev
/sbin/mkdosfs
/sbin/mkfs.reiser
/sbin/mkfs.vfat
/sbin/mkswap
/sbin/ntpd
/sbin/pivot_root
/sbin/popmaildir
/sbin/poweroff
/sbin/raidautorun
/sbin/reboot
/sbin/rdate
/sbin/rdev
/sbin/readprofile
/sbin/route
/sbin/runlevel
/sbin/sendmail
/sbin/setconsole
/sbin/setfont
/sbin/setlogcons
/sbin/sulogin
/sbin/swapoff
/sbin/swapon
/sbin/switch_root
/sbin/sysctl
/sbin/syslogd
/sbin/ubiattach
/sbin/ubidetach
/sbin/ubimkvol
/sbin/ubirmvol
/sbin/ubirsvol
/sbin/ubiupdatevol
/sbin/watchdog

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 1.19.4-1
- Initial version

