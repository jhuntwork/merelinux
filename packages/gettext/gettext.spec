Summary: GNU Gettext
Name: gettext
Version: 0.18.1.1 
Release: 3
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gettext
Source0: http://ftp.gnu.org/gnu/gettext/gettext-0.18.1.1.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 5009deb02f67fc3c59c8ce6b82408d1d35d4e38f
BuildRequires: ncurses-devel

%description
The GNU `gettext' utilities are a set of tools that provides a framework to help
other GNU packages produce multi-lingual messages

%package devel
Summary: Provides headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Provides headers and libraries for developing with %{name}

%package doc
Summary: Extensive documentation on how to implement gettext in development
Group: Development/Documentation
Requires: %{name}

%description doc
Extensive documentation on how to implement gettext in development

%prep
%setup -q

%build
export CFLAGS="-Os -pipe"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}-runtime
%find_lang %{name}-tools
cat %{name}-runtime.lang %{name}-tools.lang > %{name}.lang
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post
/usr/bin/install-info /usr/share/info/gettext.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/autosprintf.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/gettext.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/autosprintf.info /usr/share/info/dir

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/autopoint
/usr/bin/envsubst
/usr/bin/gettext
/usr/bin/gettext.sh
/usr/bin/gettextize
/usr/bin/msgattrib
/usr/bin/msgcat
/usr/bin/msgcmp
/usr/bin/msgcomm
/usr/bin/msgconv
/usr/bin/msgen
/usr/bin/msgexec
/usr/bin/msgfilter
/usr/bin/msgfmt
/usr/bin/msggrep
/usr/bin/msginit
/usr/bin/msgmerge
/usr/bin/msgunfmt
/usr/bin/msguniq
/usr/bin/ngettext
/usr/bin/recode-sr-latin
/usr/bin/xgettext
/usr/%{_lib}/gettext
/usr/%{_lib}/libasprintf.so.*
/usr/%{_lib}/libgettextpo.so.*
/usr/%{_lib}/libgettextlib-0.18.1.so
/usr/%{_lib}/libgettextsrc-0.18.1.so
/usr/%{_lib}/preloadable_libintl.so
/usr/share/doc/libasprintf
%dir /usr/share/gettext
/usr/share/gettext/ABOUT-NLS
/usr/share/gettext/po
/usr/share/gettext/styles
/usr/share/info/autosprintf.info
/usr/share/info/gettext.info
/usr/share/man/man1/*

%files devel
%defattr(-,root,root)
/usr/include/autosprintf.h
/usr/include/gettext-po.h
/usr/%{_lib}/libasprintf.a
/usr/%{_lib}/libasprintf.la
/usr/%{_lib}/libasprintf.so
/usr/%{_lib}/libgettextlib.la
/usr/%{_lib}/libgettextlib.so
/usr/%{_lib}/libgettextpo.a
/usr/%{_lib}/libgettextpo.la
/usr/%{_lib}/libgettextpo.so
/usr/%{_lib}/libgettextsrc.la
/usr/%{_lib}/libgettextsrc.so
/usr/share/aclocal/*
/usr/share/gettext/intl
/usr/share/gettext/archive.dir.tar.gz
/usr/share/gettext/config.rpath
/usr/share/gettext/gettext.h
/usr/share/gettext/javaversion.class
/usr/share/gettext/msgunfmt.tcl
/usr/share/man/man3/*

%files doc
%defattr(-,root,root)
/usr/share/doc/gettext
/usr/share/gettext/projects

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.18.1.1-3
- Optimize for size
- Build without external libxml2 support

* Mon Sep 06 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.18.1.1-2
- Better organize subpackages

* Sun Jul 18 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.18.1.1-1
- Upgrade to 0.18.1.1

* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.17-1
- Initial version
