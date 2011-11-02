Summary: Apache Portable Runtime
Name: apr
Version: 1.4.5
Release: 1
Group: System Environment/Libraries
License: Apache
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://apr.apache.org
Source0: http://apache.tradebit.com/pub//apr/apr-1.4.5.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 517de5e3cc1e3be810d9bc95508ab66bb8ebe7cb

%description
Apache project core software libraries

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-installbuilddir=/usr/share/apr-1
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
%{strip}

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libapr-1.so.*

%files devel
%defattr(-,root,root)
/usr/bin/apr-1-config
/usr/include/apr-1
/usr/%{_lib}/apr.exp
/usr/%{_lib}/libapr-1.a
/usr/%{_lib}/libapr-1.la
/usr/%{_lib}/libapr-1.so
/usr/%{_lib}/pkgconfig/apr-1.pc
/usr/share/apr-1

%changelog
* Wed Nov 02 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.5-1
- Upgrade to 1.4.5
- Optimize for size

* Wed Apr 14 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4.2-1
- Initial version
