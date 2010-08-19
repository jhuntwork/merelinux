Summary: CrackLib
Name: cracklib
Version: 2.8.16
Release: 2
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://cracklib.sourceforge.net
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-words-20080507.gz

Requires: base-layout, glibc, zlib
BuildRequires: digest(%{SOURCE0}) = 3bfb22db8fcffd019463ee415a1b25b7
BuildRequires: digest(%{SOURCE1}) = 7fa6ba0cd50e7f9ccaf4707c810b14f1
BuildRequires: zlib-devel, Python-devel

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
Requires: %{name} = %{version}

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
ln -v -sf ../../%{_lib}/libcrack.so.2.8.1 %{buildroot}/usr/%{_lib}/libcrack.so
install -v -m644 -D %{SOURCE1} %{buildroot}/usr/share/dict/cracklib-words.gz
gunzip -fv %{buildroot}/usr/share/dict/cracklib-words.gz
ln -svf cracklib-words %{buildroot}/usr/share/dict/words
%find_lang %{name}

%post
/usr/sbin/create-cracklib-dict /usr/share/dict/cracklib-words >/dev/null 2>&1

%postun
/bin/rm -rf /%{_lib}/cracklib

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/%{_lib}/libcrack.so.2
/%{_lib}/libcrack.so.2.8.1
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
/usr/lib/python2.7/site-packages/_cracklibmodule.a
/usr/lib/python2.7/site-packages/_cracklibmodule.so
/usr/lib/python2.7/site-packages/_cracklibmodule.la
/usr/lib/python2.7/site-packages/cracklib.py
/usr/lib/python2.7/site-packages/cracklib.pyc
/usr/lib/python2.7/site-packages/cracklib.pyo

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libcrack.a
/usr/%{_lib}/libcrack.so
/usr/%{_lib}/libcrack.la
/usr/include/crack.h
/usr/include/packer.h

%changelog
* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.16-2
- Fixes to dependencies and ambiguous postun command.

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.16-1
- Upgrade to 2.8.16

* Tue Sep 8 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.13-1
- Initial version
