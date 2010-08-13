Summary: Boost C++ Libraries
Name: boost
Version: 1.43.0
Release: 1
Group: Development/Tools
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.boost.org
Source: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2

Requires: base-layout, glibc, zlib, Python, bzip2
BuildRequires: digest(%{SOURCE0}) = dd49767bfb726b0c774f7db0cef91ed1
BuildRequires: zlib-devel, Python-devel, bzip2-devel

%description
Boost provides free peer-reviewed portable C++ source libraries.

%package devel
Summary: Headers and libraries for developing with %{name}
Group: Development/Libraries
Requires: %{name}

%description devel
Headers and libraries for developing with %{name}

%prep
%setup -q -n %{name}_1_43_0

%build
./bootstrap.sh \
  --prefix=/usr \
  --libdir=/usr/%{_lib}

%install
./bjam \
  --prefix=%{buildroot}/usr \
  --libdir=%{buildroot}/usr/%{_lib} \
  install

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root)
/usr/%{_lib}/libboost_date_time.so.1.43.0
/usr/%{_lib}/libboost_filesystem.so.1.43.0
/usr/%{_lib}/libboost_graph.so.1.43.0
/usr/%{_lib}/libboost_iostreams.so.1.43.0
/usr/%{_lib}/libboost_math_c99.so.1.43.0
/usr/%{_lib}/libboost_math_c99f.so.1.43.0
/usr/%{_lib}/libboost_math_c99l.so.1.43.0
/usr/%{_lib}/libboost_math_tr1.so.1.43.0
/usr/%{_lib}/libboost_math_tr1f.so.1.43.0
/usr/%{_lib}/libboost_math_tr1l.so.1.43.0
/usr/%{_lib}/libboost_prg_exec_monitor.so.1.43.0
/usr/%{_lib}/libboost_program_options.so.1.43.0
/usr/%{_lib}/libboost_python.so.1.43.0
/usr/%{_lib}/libboost_random.so.1.43.0
/usr/%{_lib}/libboost_regex.so.1.43.0
/usr/%{_lib}/libboost_serialization.so.1.43.0
/usr/%{_lib}/libboost_signals.so.1.43.0
/usr/%{_lib}/libboost_system.so.1.43.0
/usr/%{_lib}/libboost_test_exec_monitor.a
/usr/%{_lib}/libboost_thread.so.1.43.0
/usr/%{_lib}/libboost_unit_test_framework.so.1.43.0
/usr/%{_lib}/libboost_wave.so.1.43.0
/usr/%{_lib}/libboost_wserialization.so.1.43.0

%files devel
%defattr(-,root,root)
/usr/include/boost
/usr/%{_lib}/libboost_date_time.a
/usr/%{_lib}/libboost_date_time.so
/usr/%{_lib}/libboost_filesystem.a
/usr/%{_lib}/libboost_filesystem.so
/usr/%{_lib}/libboost_graph.a
/usr/%{_lib}/libboost_graph.so
/usr/%{_lib}/libboost_iostreams.a
/usr/%{_lib}/libboost_iostreams.so
/usr/%{_lib}/libboost_math_c99.a
/usr/%{_lib}/libboost_math_c99.so
/usr/%{_lib}/libboost_math_c99f.a
/usr/%{_lib}/libboost_math_c99f.so
/usr/%{_lib}/libboost_math_c99l.a
/usr/%{_lib}/libboost_math_c99l.so
/usr/%{_lib}/libboost_math_tr1.a
/usr/%{_lib}/libboost_math_tr1.so
/usr/%{_lib}/libboost_math_tr1f.a
/usr/%{_lib}/libboost_math_tr1f.so
/usr/%{_lib}/libboost_math_tr1l.a
/usr/%{_lib}/libboost_math_tr1l.so
/usr/%{_lib}/libboost_prg_exec_monitor.a
/usr/%{_lib}/libboost_prg_exec_monitor.so
/usr/%{_lib}/libboost_program_options.a
/usr/%{_lib}/libboost_program_options.so
/usr/%{_lib}/libboost_python.a
/usr/%{_lib}/libboost_python.so
/usr/%{_lib}/libboost_random.a
/usr/%{_lib}/libboost_random.so
/usr/%{_lib}/libboost_regex.a
/usr/%{_lib}/libboost_regex.so
/usr/%{_lib}/libboost_serialization.a
/usr/%{_lib}/libboost_serialization.so
/usr/%{_lib}/libboost_signals.a
/usr/%{_lib}/libboost_signals.so
/usr/%{_lib}/libboost_system.a
/usr/%{_lib}/libboost_system.so
/usr/%{_lib}/libboost_thread.a
/usr/%{_lib}/libboost_thread.so
/usr/%{_lib}/libboost_unit_test_framework.a
/usr/%{_lib}/libboost_unit_test_framework.so
/usr/%{_lib}/libboost_wave.a
/usr/%{_lib}/libboost_wave.so
/usr/%{_lib}/libboost_wserialization.a
/usr/%{_lib}/libboost_wserialization.so

%changelog
* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.43.0-1
- Initial version
