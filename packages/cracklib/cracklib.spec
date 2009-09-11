Summary: CrackLib
Name: cracklib
Version: 2.8.13
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://cracklib.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-words-20080507.gz

Requires: base-layout, glibc

%description
A Next generation version of the libCrack password checking library.

%package python
Summary: %{name} modules for Python
Group: Development/Modules
Requires: %{name} = %{version}

%description python
%{name} modules for python

%package devel
Summary: Files for developing with %{name}
Group: Development/Libraries
Requires: %{name} = ${version}

%description devel
Libraries and Header files for developing with %{name}

%prep
%setup -q

%build
./configure --prefix=/usr --libdir=/usr/%{_lib} \
 --with-default-dict=/%{_lib}/cracklib/pw_dict
make

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_lib}/cracklib
mv -v %{buildroot}/usr/%{_lib}/libcrack.so.2* %{buildroot}/%{_lib}
ln -v -sf ../../%{_lib}/libcrack.so.2.8.0 %{buildroot}/usr/%{_lib}/libcrack.so
install -v -m644 -D %{SOURCE1} %{buildroot}/usr/share/dict/cracklib-words.gz
gunzip -fv %{buildroot}/usr/share/dict/cracklib-words.gz
ln -svf cracklib-words %{buildroot}/usr/share/dict/words
install -v -m755 -d %{buildroot}/lib/cracklib
find %{buildroot} -name "*.la" -exec rm -vf '{}' \;
%find_lang %{name}

%post
/usr/sbin/create-cracklib-dict /usr/share/dict/cracklib-words >/dev/null 2>&1

%postun
rm -rf /%{_lib}/cracklib

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/%{_lib}/libcrack.so.2
/%{_lib}/libcrack.so.2.8.0
/%{_lib}/cracklib
/usr/sbin/cracklib-check
/usr/sbin/cracklib-format
/usr/sbin/cracklib-packer
/usr/sbin/cracklib-unpacker
/usr/sbin/create-cracklib-dict
/usr/share/cracklib
/usr/share/dict/cracklib-words
/usr/share/dict/words

%files python
%defattr(-,root,root)
/usr/%{_lib}/python2.6/site-packages/_cracklibmodule.a
/usr/%{_lib}/python2.6/site-packages/_cracklibmodule.so
/usr/%{_lib}/python2.6/site-packages/cracklib.py
/usr/%{_lib}/python2.6/site-packages/cracklib.pyc
/usr/%{_lib}/python2.6/site-packages/cracklib.pyo

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libcrack.a
/usr/%{_lib}/libcrack.so
/usr/include/crack.h
/usr/include/packer.h

%changelog
* Tue Sep 8 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.13-1
- Initial version
