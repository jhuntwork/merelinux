Summary: uClibc: A C library for embedded Linux
Name: uclibc
Version: 0.9.32
Release: 1
Group: System Environment/Libraries
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://uclibc.org
Source0: http://uclibc.org/downloads/uClibc-%{version}.tar.xz
Source1: uclibc-config

BuildRequires: digest(sha1:%{SOURCE0}) = fe38ca462d4284cfcd7458cfc820db7909ad4ab8
BuildRequires: digest(sha1:%{SOURCE1}) = c558a045aef77201ea983d945037e96e6b2ffc6e

%description
uClibc (aka µClibc/pronounced yew-see-lib-see) is a C library for developin
embedded Linux systems. It is much smaller than the GNU C Library, but nearly
all applications supported by glibc also work perfectly with uClibc. Porting
applications from glibc to uClibc typically involves just recompiling the
source code. uClibc even supports shared libraries and threading.

%package devel
Summary: Headers, object files and utilities for development using C libraries
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
The %{name}-devel package contains the object files necessary for
developing programs which use the standard C libraries (which are used
by nearly all programs).  If you are developing programs which will use
the standard C libraries, your system needs to have these standard
object files available in order to create the executables.

%prep
%setup -q -n uClibc-%{version}

%build
cp %{SOURCE1} .config
make V=2 %{PMFLAGS}
make V=2 %{PMFLAGS} utils

%install
make V=1 PREFIX=%{buildroot} install
make V=1 PREFIX=%{buildroot} install_utils
#%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/lib/ld64-uClibc-%{version}.so
/lib/ld64-uClibc.so.0
/lib/libc.so.0
/lib/libcrypt-%{version}.so
/lib/libcrypt.so.0
/lib/libdl-%{version}.so
/lib/libdl.so.0
/lib/libm-%{version}.so
/lib/libm.so.0
/lib/libpthread-%{version}.so
/lib/libpthread.so.0
/lib/librt-%{version}.so
/lib/librt.so.0
/lib/libuClibc-%{version}.so
/usr/bin/getconf
/usr/bin/ldd
/sbin/ldconfig

%files devel
%defattr(-,root,root)
/usr/include/a.out.h
/usr/include/alloca.h
/usr/include/ar.h
%dir /usr/include/arpa
/usr/include/arpa/ftp.h
/usr/include/arpa/inet.h
/usr/include/arpa/nameser.h
/usr/include/arpa/nameser_compat.h
/usr/include/arpa/telnet.h
/usr/include/arpa/tftp.h
/usr/include/assert.h
/usr/include/atomic.h
%dir /usr/include/bits
/usr/include/bits/atomic.h
/usr/include/bits/byteswap-common.h
/usr/include/bits/byteswap.h
/usr/include/bits/cmathcalls.h
/usr/include/bits/confname.h
/usr/include/bits/dirent.h
/usr/include/bits/dlfcn.h
/usr/include/bits/elfclass.h
/usr/include/bits/endian.h
/usr/include/bits/environments.h
/usr/include/bits/errno.h
/usr/include/bits/fcntl.h
/usr/include/bits/fenv.h
/usr/include/bits/fenvinline.h
/usr/include/bits/getopt.h
/usr/include/bits/huge_val.h
/usr/include/bits/huge_valf.h
/usr/include/bits/huge_vall.h
/usr/include/bits/in.h
/usr/include/bits/inf.h
/usr/include/bits/initspin.h
/usr/include/bits/ioctl-types.h
/usr/include/bits/ioctls.h
/usr/include/bits/ipc.h
/usr/include/bits/kernel-features.h
/usr/include/bits/libc-lock.h
/usr/include/bits/local_lim.h
/usr/include/bits/locale.h
/usr/include/bits/mathcalls.h
/usr/include/bits/mathdef.h
/usr/include/bits/mathinline.h
/usr/include/bits/mman-common.h
/usr/include/bits/mman.h
/usr/include/bits/mqueue.h
/usr/include/bits/msq.h
/usr/include/bits/nan.h
/usr/include/bits/netdb.h
/usr/include/bits/poll.h
/usr/include/bits/posix1_lim.h
/usr/include/bits/posix2_lim.h
/usr/include/bits/posix_opt.h
/usr/include/bits/pthreadtypes.h
/usr/include/bits/resource.h
/usr/include/bits/sched.h
/usr/include/bits/select.h
/usr/include/bits/sem.h
/usr/include/bits/semaphore.h
/usr/include/bits/setjmp.h
/usr/include/bits/shm.h
/usr/include/bits/sigaction.h
/usr/include/bits/sigcontext.h
/usr/include/bits/siginfo.h
/usr/include/bits/signum.h
/usr/include/bits/sigset.h
/usr/include/bits/sigstack.h
/usr/include/bits/sigthread.h
/usr/include/bits/sockaddr.h
/usr/include/bits/socket.h
/usr/include/bits/stat.h
/usr/include/bits/statfs.h
/usr/include/bits/statvfs.h
/usr/include/bits/stdio-lock.h
/usr/include/bits/stdio.h
/usr/include/bits/stdio_lim.h
/usr/include/bits/sysnum.h
/usr/include/bits/termios.h
/usr/include/bits/time.h
/usr/include/bits/types.h
/usr/include/bits/typesizes.h
/usr/include/bits/uClibc_alloc.h
/usr/include/bits/uClibc_charclass.h
/usr/include/bits/uClibc_clk_tck.h
/usr/include/bits/uClibc_config.h
/usr/include/bits/uClibc_local_lim.h
/usr/include/bits/uClibc_locale.h
/usr/include/bits/uClibc_mutex.h
/usr/include/bits/uClibc_page.h
/usr/include/bits/uClibc_pthread.h
/usr/include/bits/uClibc_stdio.h
/usr/include/bits/uClibc_touplow.h
/usr/include/bits/uio.h
/usr/include/bits/utmp.h
/usr/include/bits/utmpx.h
/usr/include/bits/utsname.h
/usr/include/bits/waitflags.h
/usr/include/bits/waitstatus.h
/usr/include/bits/wchar.h
/usr/include/bits/wordsize.h
/usr/include/bits/xopen_lim.h
/usr/include/byteswap.h
/usr/include/complex.h
/usr/include/cpio.h
/usr/include/crypt.h
/usr/include/ctype.h
/usr/include/dirent.h
/usr/include/dlfcn.h
/usr/include/elf.h
/usr/include/endian.h
/usr/include/errno.h
/usr/include/error.h
/usr/include/err.h
/usr/include/fcntl.h
/usr/include/features.h
/usr/include/fenv.h
/usr/include/fnmatch.h
/usr/include/fpu_control.h
/usr/include/fts.h
/usr/include/getopt.h
/usr/include/glob.h
/usr/include/gnu-versions.h
/usr/include/grp.h
/usr/include/ieee754.h
%dir /usr/include/internal
/usr/include/internal/parse_config.h
/usr/include/inttypes.h
/usr/include/langinfo.h
/usr/include/lastlog.h
/usr/include/libgen.h
/usr/include/limits.h
/usr/include/link.h
/usr/include/locale.h
/usr/include/malloc.h
/usr/include/math.h
/usr/include/memory.h
/usr/include/mntent.h
/usr/include/mqueue.h
%dir /usr/include/net
/usr/include/net/ethernet.h
/usr/include/net/if.h
/usr/include/net/if_arp.h
/usr/include/net/if_packet.h
/usr/include/net/if_ppp.h
/usr/include/net/if_shaper.h
/usr/include/net/if_slip.h
/usr/include/net/ppp-comp.h
/usr/include/net/ppp_defs.h
/usr/include/net/route.h
%dir /usr/include/netax25
/usr/include/netax25/ax25.h
/usr/include/netdb.h
%dir /usr/include/neteconet
/usr/include/neteconet/ec.h
%dir /usr/include/netinet
/usr/include/netinet/ether.h
/usr/include/netinet/icmp6.h
/usr/include/netinet/if_ether.h
/usr/include/netinet/if_fddi.h
/usr/include/netinet/if_tr.h
/usr/include/netinet/igmp.h
/usr/include/netinet/in.h
/usr/include/netinet/in_systm.h
/usr/include/netinet/ip.h
/usr/include/netinet/ip6.h
/usr/include/netinet/ip_icmp.h
/usr/include/netinet/tcp.h
/usr/include/netinet/udp.h
%dir /usr/include/netipx
/usr/include/netipx/ipx.h
%dir /usr/include/netpacket
/usr/include/netpacket/packet.h
/usr/include/nl_types.h
/usr/include/obstack.h
/usr/include/paths.h
/usr/include/poll.h
%dir /usr/include/protocols
/usr/include/protocols/routed.h
/usr/include/protocols/rwhod.h
/usr/include/protocols/talkd.h
/usr/include/protocols/timed.h
/usr/include/pthread.h
/usr/include/pty.h
/usr/include/pwd.h
/usr/include/regex.h
/usr/include/regexp.h
/usr/include/resolv.h
/usr/include/sched.h
%dir /usr/include/scsi
/usr/include/scsi/scsi.h
/usr/include/scsi/scsi_ioctl.h
/usr/include/scsi/sg.h
/usr/include/search.h
/usr/include/semaphore.h
/usr/include/setjmp.h
/usr/include/sgtty.h
/usr/include/shadow.h
/usr/include/signal.h
/usr/include/stdint.h
/usr/include/stdio.h
/usr/include/stdio_ext.h
/usr/include/stdlib.h
/usr/include/string.h
/usr/include/strings.h
%dir /usr/include/sys
/usr/include/sys/acct.h
/usr/include/sys/bitypes.h
/usr/include/sys/cdefs.h
/usr/include/sys/debugreg.h
/usr/include/sys/dir.h
/usr/include/sys/epoll.h
/usr/include/sys/errno.h
/usr/include/sys/fcntl.h
/usr/include/sys/file.h
/usr/include/sys/fsuid.h
/usr/include/sys/inotify.h
/usr/include/sys/io.h
/usr/include/sys/ioctl.h
/usr/include/sys/ipc.h
/usr/include/sys/kd.h
/usr/include/sys/kdaemon.h
/usr/include/sys/klog.h
/usr/include/sys/mman.h
/usr/include/sys/mount.h
/usr/include/sys/msg.h
/usr/include/sys/mtio.h
/usr/include/sys/param.h
/usr/include/sys/perm.h
/usr/include/sys/personality.h
/usr/include/sys/poll.h
/usr/include/sys/prctl.h
/usr/include/sys/procfs.h
/usr/include/sys/ptrace.h
/usr/include/sys/queue.h
/usr/include/sys/quota.h
/usr/include/sys/reboot.h
/usr/include/sys/reg.h
/usr/include/sys/resource.h
/usr/include/sys/select.h
/usr/include/sys/sem.h
/usr/include/sys/sendfile.h
/usr/include/sys/shm.h
/usr/include/sys/signal.h
/usr/include/sys/signalfd.h
/usr/include/sys/socket.h
/usr/include/sys/socketvar.h
/usr/include/sys/soundcard.h
/usr/include/sys/stat.h
/usr/include/sys/statfs.h
/usr/include/sys/statvfs.h
/usr/include/sys/swap.h
/usr/include/sys/syscall.h
/usr/include/sys/sysctl.h
/usr/include/sys/sysinfo.h
/usr/include/sys/syslog.h
/usr/include/sys/sysmacros.h
/usr/include/sys/termios.h
/usr/include/sys/time.h
/usr/include/sys/timeb.h
/usr/include/sys/timerfd.h
/usr/include/sys/times.h
/usr/include/sys/timex.h
/usr/include/sys/ttydefaults.h
/usr/include/sys/types.h
/usr/include/sys/ucontext.h
/usr/include/sys/uio.h
/usr/include/sys/un.h
/usr/include/sys/unistd.h
/usr/include/sys/user.h
/usr/include/sys/utsname.h
/usr/include/sys/vfs.h
/usr/include/sys/vt.h
/usr/include/sys/wait.h
/usr/include/syscall.h
/usr/include/sysexits.h
/usr/include/syslog.h
/usr/include/tar.h
/usr/include/termio.h
/usr/include/termios.h
/usr/include/tgmath.h
/usr/include/time.h
/usr/include/ttyent.h
/usr/include/ucontext.h
/usr/include/ulimit.h
/usr/include/unistd.h
/usr/include/utime.h
/usr/include/utmp.h
/usr/include/utmpx.h
/usr/include/values.h
/usr/include/wait.h
/usr/include/wchar.h
/usr/include/wctype.h
/usr/lib/Scrt1.o
/usr/lib/crt1.o
/usr/lib/crti.o
/usr/lib/crtn.o
/usr/lib/libc.a
/usr/lib/libc.so
/usr/lib/libcrypt.a
/usr/lib/libcrypt.so
/usr/lib/libdl.a
/usr/lib/libdl.so
/usr/lib/libm.a
/usr/lib/libm.so
/usr/lib/libpthread.a
/usr/lib/libpthread.so
/usr/lib/libpthread_nonshared.a
/usr/lib/librt.a
/usr/lib/librt.so
/usr/lib/uclibc_nonshared.a

%changelog
* Sat Dec 10 2011 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 0.9.32-1
- Initial version
