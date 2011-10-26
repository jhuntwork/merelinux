Summary: libpipeline - pipeline manipulation library
Name: libpipeline
Version: 1.2.0
Release: 1
Group: System Environment/Libraries
License: GPLv3
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://libpipeline.nongnu.org
Source0: http://gnu.mirrors.pair.com/savannah/savannah/libpipeline/libpipeline-1.2.0.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 85638517d393c98465f7693f02afb4d02ed0f959

%description
libpipeline is a C library for manipulating pipelines of subprocesses in a
flexible and convenient way.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libpipeline.so.*

%files devel
%defattr(-,root,root)
/usr/include/pipeline.h
/usr/%{_lib}/libpipeline.la
/usr/%{_lib}/libpipeline.so
/usr/%{_lib}/pkgconfig/libpipeline.pc
/usr/share/man/man3/libpipeline.3.bz2
/usr/share/man/man3/pipecmd_arg.3.bz2
/usr/share/man/man3/pipecmd_argf.3.bz2
/usr/share/man/man3/pipecmd_args.3.bz2
/usr/share/man/man3/pipecmd_argstr.3.bz2
/usr/share/man/man3/pipecmd_argv.3.bz2
/usr/share/man/man3/pipecmd_clearenv.3.bz2
/usr/share/man/man3/pipecmd_discard_err.3.bz2
/usr/share/man/man3/pipecmd_dump.3.bz2
/usr/share/man/man3/pipecmd_dup.3.bz2
/usr/share/man/man3/pipecmd_exec.3.bz2
/usr/share/man/man3/pipecmd_free.3.bz2
/usr/share/man/man3/pipecmd_get_nargs.3.bz2
/usr/share/man/man3/pipecmd_new.3.bz2
/usr/share/man/man3/pipecmd_new_args.3.bz2
/usr/share/man/man3/pipecmd_new_argstr.3.bz2
/usr/share/man/man3/pipecmd_new_argv.3.bz2
/usr/share/man/man3/pipecmd_new_function.3.bz2
/usr/share/man/man3/pipecmd_new_passthrough.3.bz2
/usr/share/man/man3/pipecmd_new_sequence.3.bz2
/usr/share/man/man3/pipecmd_nice.3.bz2
/usr/share/man/man3/pipecmd_sequence_command.3.bz2
/usr/share/man/man3/pipecmd_setenv.3.bz2
/usr/share/man/man3/pipecmd_tostring.3.bz2
/usr/share/man/man3/pipecmd_unsetenv.3.bz2
/usr/share/man/man3/pipeline_command.3.bz2
/usr/share/man/man3/pipeline_command_args.3.bz2
/usr/share/man/man3/pipeline_command_argstr.3.bz2
/usr/share/man/man3/pipeline_commands.3.bz2
/usr/share/man/man3/pipeline_commandv.3.bz2
/usr/share/man/man3/pipeline_connect.3.bz2
/usr/share/man/man3/pipeline_dump.3.bz2
/usr/share/man/man3/pipeline_free.3.bz2
/usr/share/man/man3/pipeline_get_command.3.bz2
/usr/share/man/man3/pipeline_get_infile.3.bz2
/usr/share/man/man3/pipeline_get_ncommands.3.bz2
/usr/share/man/man3/pipeline_get_outfile.3.bz2
/usr/share/man/man3/pipeline_get_pid.3.bz2
/usr/share/man/man3/pipeline_ignore_signals.3.bz2
/usr/share/man/man3/pipeline_install_post_fork.3.bz2
/usr/share/man/man3/pipeline_join.3.bz2
/usr/share/man/man3/pipeline_new.3.bz2
/usr/share/man/man3/pipeline_new_command_args.3.bz2
/usr/share/man/man3/pipeline_new_commands.3.bz2
/usr/share/man/man3/pipeline_new_commandv.3.bz2
/usr/share/man/man3/pipeline_peek.3.bz2
/usr/share/man/man3/pipeline_peek_size.3.bz2
/usr/share/man/man3/pipeline_peek_skip.3.bz2
/usr/share/man/man3/pipeline_peekline.3.bz2
/usr/share/man/man3/pipeline_pump.3.bz2
/usr/share/man/man3/pipeline_read.3.bz2
/usr/share/man/man3/pipeline_readline.3.bz2
/usr/share/man/man3/pipeline_set_command.3.bz2
/usr/share/man/man3/pipeline_start.3.bz2
/usr/share/man/man3/pipeline_tostring.3.bz2
/usr/share/man/man3/pipeline_wait.3.bz2
/usr/share/man/man3/pipeline_want_in.3.bz2
/usr/share/man/man3/pipeline_want_infile.3.bz2
/usr/share/man/man3/pipeline_want_out.3.bz2
/usr/share/man/man3/pipeline_want_outfile.3.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntowrk@lightcubesolutions.com> - 1.2.0-1
- Initial version
