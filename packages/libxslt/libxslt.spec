Summary: The XSLT C library for GNOME
Name: libxslt
Version: 1.1.26
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.xmlsoft.org/XSLT
Source0: ftp://xmlsoft.org/libxslt/libxslt-1.1.26.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 69f74df8228b504a87e2b257c2d5238281c65154
BuildRequires: libxml2-devel
BuildRequires: libxml2-python
BuildRequires: python-devel
BuildRequires: libgcrypt-devel
BuildRequires: libgpg-error-devel
BuildRequires: zlib-devel

%description
Libxslt is the XSLT C library developed for the GNOME project. XSLT itself is
a an XML language to define transformation for XML. Libxslt is based on
libxml2 the XML C library developed for the GNOME project. It also implements
most of the EXSLT set of processor-portable extensions functions and some of
Saxon's evaluate and expressions extensions.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%package python
Summary: Libraries for developing with libxslt in Python
Group: Development/Libraries
Requires: %{name}, python(abi) = 2.7

%description python
Libraries for developing with libxslt in python

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
/usr/bin/xsltproc
/usr/%{_lib}/libexslt.so.0
/usr/%{_lib}/libexslt.so.0.8.15
/usr/%{_lib}/libxslt.so.1
/usr/%{_lib}/libxslt.so.1.1.26
/usr/share/man/man1/xsltproc.1.bz2

%files devel
%defattr(-,root,root)
/usr/bin/xslt-config
/usr/include/libexslt
/usr/include/libxslt
/usr/%{_lib}/libexslt.a
/usr/%{_lib}/libexslt.la
/usr/%{_lib}/libexslt.so
/usr/%{_lib}/libxslt.a
/usr/%{_lib}/libxslt.la
/usr/%{_lib}/libxslt.so
/usr/%{_lib}/pkgconfig/libexslt.pc
/usr/%{_lib}/pkgconfig/libxslt.pc
/usr/%{_lib}/xsltConf.sh
/usr/share/aclocal/libxslt.m4
/usr/share/doc/libxslt-%{version}
/usr/share/man/man3/libexslt.3.bz2
/usr/share/man/man3/libxslt.3.bz2

%files python
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/libxslt.py
/usr/lib/python2.7/site-packages/libxsltmod.a
/usr/lib/python2.7/site-packages/libxsltmod.la
/usr/lib/python2.7/site-packages/libxsltmod.so
/usr/share/doc/libxslt-python-%{version}

%changelog
* Sun Oct 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.26-2
- Optimize for size

* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.1.26-1
- Initial version
