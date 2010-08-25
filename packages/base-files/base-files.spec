Summary: Essential System Files
Name: base-files
Version: 0.1
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch

Requires: base-layout

%description
Provides core files needed by the base system.

%install
install -dv %{buildroot}/{etc,dev,var}
install -dv %{buildroot}/var/{run,log}
cat > %{buildroot}/etc/passwd << "EOF"
root:x:0:0:root:/root:/bin/bash
bin:x:1:1:bin:/dev/null:/bin/false
fcron:x:22:22:fcron:/dev/null:/bin/false
apache:x:25:25:apache:/dev/null:/bin/false
nginx:x:26:26:apache:/dev/null:/bin/false
postfix:x:32:32:postfix:/dev/null:/bin/false
mysql:x:40:40:mysql:/dev/null:/bin/false
ftp:x:45:45:ftp:/srv/ftp:/bin/false
vsftpd:x:47:47:vsftpd:/dev/null:/bin/false
rsyncd:x:48:48:rsyncd:/dev/null:/bin/false
sshd:x:50:50:sshd:/var/lib/sshd:/bin/false
nobody:x:99:99:nobody:/dev/null:/bin/false
EOF
cat > %{buildroot}/etc/group << "EOF"
root:x:0:
bin:x:1:
sys:x:2:
kmem:x:3:
tty:x:4:
tape:x:5:
daemon:x:6:
floppy:x:7:
disk:x:8:
lp:x:9:
dialout:x:10:
audio:x:11:
video:x:12:
utmp:x:13:
usb:x:14:
cdrom:x:15:
fcron:x:22:
apache:x:25:
nginx:x:26:
postfix:x:32:
postdrop:x:33:
mail:x:34:
mysql:x:40:
ftp:x:45:
vsftpd:x:47:
rsyncd:x:48:
sshd:x:50:
nogroup:x:99:
EOF
cat > %{buildroot}/etc/inputrc << "EOF"
# Begin /etc/inputrc
# Modified by Chris Lynn <roryo@roryo.dynup.net>

# Make sure we dont output everything on the 1 line
set horizontal-scroll-mode Off

# Enable 8bit input
set meta-flag On 
set input-meta On

# Turns off 8th bit stripping
set convert-meta Off

# Keep the 8th bit for display
set output-meta On

# none, visible or audible
set bell-style none

# All of the following map the escape sequence of the 
# value contained inside the 1st argument to the 
# readline specific functions

"\eOd": backward-word
"\eOc": forward-word

# for linux console
"\e[1~": beginning-of-line
"\e[4~": end-of-line
"\e[5~": beginning-of-history
"\e[6~": end-of-history
"\e[3~": delete-char
"\e[2~": quoted-insert

# for xterm
"\eOH": beginning-of-line
"\eOF": end-of-line

# for Konsole
"\e[H": beginning-of-line
"\e[F": end-of-line

# End /etc/inputrc
EOF
install -dv %{buildroot}/{dev,etc,var}
install -dv %{buildroot}/var/{log,run}
mknod -m 600 %{buildroot}/dev/console c 5 1
mknod -m 666 %{buildroot}/dev/null c 1 3
touch %{buildroot}/etc/mtab
touch %{buildroot}/var/run/utmp
touch %{buildroot}/var/log/{btmp,lastlog,wtmp}

%files
%defattr(-,root,root)
/dev/console
/dev/null
/etc/passwd
/etc/group
/etc/inputrc
/etc/mtab
/var/log/btmp
/var/log/wtmp
%defattr(0664,root,utmp)
/var/log/lastlog
/var/run/utmp

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-2
- Add nginx user and group.

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Add inputrc file. Increment local version.

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-1
- Initial version
