Summary: libxml2 XML toolkit
Name: libxml2
Version: 2.7.8
Release: 1
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.xmlsoft.org
Source0: ftp://xmlsoft.org/libxml2/libxml2-2.7.8.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 859dd535edbb851cc15b64740ee06551a7a17d40
BuildRequires: Python-devel
BuildRequires: zlib-devel

%description
Libxml2 is the XML C parser and toolkit developed for the Gnome project
(but usable outside of the Gnome platform)

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for developing with libxml2 in Python
Group: Development/Libraries
Requires: %{name} >= %{version}, Python >= 2.7

%description python
Libraries for developing with libxml2 in Python

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
# Don't want the gtk-doc html files
rm -rf %{buildroot}/usr/share/gtk-doc
# Force use of /usr/lib/python2.7
%if "%{_lib}" != "lib"
  install -dv %{buildroot}/usr/lib
  mv -v %{buildroot}/usr/%{_lib}/python2.7 %{buildroot}/usr/lib/
%endif
%{compress_man}
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/bin/xmlcatalog
/usr/bin/xmllint
/usr/%{_lib}/libxml2.so.2
/usr/%{_lib}/libxml2.so.2.7.8
/usr/share/man/man1/xmlcatalog.1.bz2
/usr/share/man/man1/xmllint.1.bz2

%files devel
%defattr(-,root,root)
/usr/bin/xml2-config
/usr/include/libxml2
/usr/share/aclocal/libxml.m4
/usr/%{_lib}/pkgconfig/libxml-2.0.pc
/usr/%{_lib}/xml2Conf.sh
/usr/%{_lib}/libxml2.a
/usr/%{_lib}/libxml2.la
/usr/%{_lib}/libxml2.so
/usr/share/doc/libxml2-%{version}
/usr/share/man/man1/xml2-config.1.bz2
/usr/share/man/man3/libxml.3.bz2

%files python
%defattr(-,root,root)
/usr/share/doc/libxml2-python-%{version}
/usr/lib/python2.7/site-packages/drv_libxml2.py
/usr/lib/python2.7/site-packages/libxml2.py
/usr/lib/python2.7/site-packages/libxml2mod.a
/usr/lib/python2.7/site-packages/libxml2mod.la
/usr/lib/python2.7/site-packages/libxml2mod.so

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.8-1
- Upgrade to 2.7.8
- Optimize for size

* Fri Jul 16 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.7-1
- Initial version
