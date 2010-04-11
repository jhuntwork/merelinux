Summary: GNU Gettext
Name: gettext
Version: 0.17 
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gettext
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-upstream_fixes-2.patch

Requires: base-layout, glibc
BuildRequires: digest(%{SOURCE0}) = 58a2bc6d39c0ba57823034d55d65d606
BuildRequires: digest(%{PATCH0}) = ae64b6399ed6536e148e8386bcb91689

%description
The GNU `gettext' utilities are a set of tools that provides a framework to help
other GNU packages produce multi-lingual messages

%package devel
Summary: Provides headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Provides headers and libraries for developing with %{name}

%package examples
Summary: Extensive examples on how to implement gettext in development
Group: Development/Documentation
Requires: %{name}

%description examples
Extensive examples on how to implement gettext in development

%prep
%setup -q
%patch0 -p1

%build
./configure --prefix=/usr --libdir=/usr/%{_lib}
make
make check

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}-runtime
%find_lang %{name}-tools
cat %{name}-runtime.lang %{name}-tools.lang > %{name}.lang

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
/usr/share/aclocal/codeset.m4
/usr/share/aclocal/gettext.m4
/usr/share/aclocal/glibc2.m4
/usr/share/aclocal/glibc21.m4
/usr/share/aclocal/iconv.m4
/usr/share/aclocal/intdiv0.m4
/usr/share/aclocal/intl.m4
/usr/share/aclocal/intldir.m4
/usr/share/aclocal/intlmacosx.m4
/usr/share/aclocal/intmax.m4
/usr/share/aclocal/inttypes-pri.m4
/usr/share/aclocal/inttypes_h.m4
/usr/share/aclocal/lcmessage.m4
/usr/share/aclocal/lib-ld.m4
/usr/share/aclocal/lib-link.m4
/usr/share/aclocal/lib-prefix.m4
/usr/share/aclocal/lock.m4
/usr/share/aclocal/longlong.m4
/usr/share/aclocal/nls.m4
/usr/share/aclocal/po.m4
/usr/share/aclocal/printf-posix.m4
/usr/share/aclocal/progtest.m4
/usr/share/aclocal/size_max.m4
/usr/share/aclocal/stdint_h.m4
/usr/share/aclocal/uintmax_t.m4
/usr/share/aclocal/visibility.m4
/usr/share/aclocal/wchar_t.m4
/usr/share/aclocal/wint_t.m4
/usr/share/aclocal/xsize.m4
/usr/%{_lib}/libasprintf.so.*
/usr/%{_lib}/libgettextlib-0.17.so
/usr/%{_lib}/libgettextpo.so.*
/usr/%{_lib}/libgettextsrc-0.17.so
%dir /usr/share/doc/gettext/
/usr/share/doc/gettext/FAQ.html
/usr/share/doc/gettext/autopoint.1.html
/usr/share/doc/gettext/bind_textdomain_codeset.3.html
/usr/share/doc/gettext/bindtextdomain.3.html
/usr/share/doc/gettext/envsubst.1.html
/usr/share/doc/gettext/gettext.1.html
/usr/share/doc/gettext/gettext.3.html
/usr/share/doc/gettext/gettext_1.html
/usr/share/doc/gettext/gettext_10.html
/usr/share/doc/gettext/gettext_11.html
/usr/share/doc/gettext/gettext_12.html
/usr/share/doc/gettext/gettext_13.html
/usr/share/doc/gettext/gettext_14.html
/usr/share/doc/gettext/gettext_15.html
/usr/share/doc/gettext/gettext_16.html
/usr/share/doc/gettext/gettext_17.html
/usr/share/doc/gettext/gettext_18.html
/usr/share/doc/gettext/gettext_19.html
/usr/share/doc/gettext/gettext_2.html
/usr/share/doc/gettext/gettext_20.html
/usr/share/doc/gettext/gettext_21.html
/usr/share/doc/gettext/gettext_22.html
/usr/share/doc/gettext/gettext_23.html
/usr/share/doc/gettext/gettext_24.html
/usr/share/doc/gettext/gettext_25.html
/usr/share/doc/gettext/gettext_3.html
/usr/share/doc/gettext/gettext_4.html
/usr/share/doc/gettext/gettext_5.html
/usr/share/doc/gettext/gettext_6.html
/usr/share/doc/gettext/gettext_7.html
/usr/share/doc/gettext/gettext_8.html
/usr/share/doc/gettext/gettext_9.html
/usr/share/doc/gettext/gettext_foot.html
/usr/share/doc/gettext/gettext_toc.html
/usr/share/doc/gettext/gettextize.1.html
/usr/share/doc/gettext/msgattrib.1.html
/usr/share/doc/gettext/msgcat.1.html
/usr/share/doc/gettext/msgcmp.1.html
/usr/share/doc/gettext/msgcomm.1.html
/usr/share/doc/gettext/msgconv.1.html
/usr/share/doc/gettext/msgen.1.html
/usr/share/doc/gettext/msgexec.1.html
/usr/share/doc/gettext/msgfilter.1.html
/usr/share/doc/gettext/msgfmt.1.html
/usr/share/doc/gettext/msggrep.1.html
/usr/share/doc/gettext/msginit.1.html
/usr/share/doc/gettext/msgmerge.1.html
/usr/share/doc/gettext/msgunfmt.1.html
/usr/share/doc/gettext/msguniq.1.html
/usr/share/doc/gettext/ngettext.1.html
/usr/share/doc/gettext/ngettext.3.html
/usr/share/doc/gettext/recode-sr-latin.1.html
/usr/share/doc/gettext/textdomain.3.html
/usr/share/doc/gettext/tutorial.html
/usr/share/doc/gettext/xgettext.1.html
/usr/share/doc/libasprintf/autosprintf_all.html
/usr/share/gettext
/usr/share/info/autosprintf.info
/usr/share/info/gettext.info
/usr/share/man/man1/autopoint.1
/usr/share/man/man1/envsubst.1
/usr/share/man/man1/gettext.1
/usr/share/man/man1/gettextize.1
/usr/share/man/man1/msgattrib.1
/usr/share/man/man1/msgcat.1
/usr/share/man/man1/msgcmp.1
/usr/share/man/man1/msgcomm.1
/usr/share/man/man1/msgconv.1
/usr/share/man/man1/msgen.1
/usr/share/man/man1/msgexec.1
/usr/share/man/man1/msgfilter.1
/usr/share/man/man1/msgfmt.1
/usr/share/man/man1/msggrep.1
/usr/share/man/man1/msginit.1
/usr/share/man/man1/msgmerge.1
/usr/share/man/man1/msgunfmt.1
/usr/share/man/man1/msguniq.1
/usr/share/man/man1/ngettext.1
/usr/share/man/man1/recode-sr-latin.1
/usr/share/man/man1/xgettext.1

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
/usr/%{_lib}/preloadable_libintl.so
/usr/share/doc/gettext/javadoc2
/usr/share/doc/gettext/csharpdoc
/usr/share/man/man3/bind_textdomain_codeset.3
/usr/share/man/man3/bindtextdomain.3
/usr/share/man/man3/dcgettext.3
/usr/share/man/man3/dcngettext.3
/usr/share/man/man3/dgettext.3
/usr/share/man/man3/dngettext.3
/usr/share/man/man3/gettext.3
/usr/share/man/man3/ngettext.3
/usr/share/man/man3/textdomain.3

%files examples
%defattr(-,root,root)
/usr/share/doc/gettext/examples

%changelog
* Sun Apr 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.17-1
- Initial version
