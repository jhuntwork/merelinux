Summary: CrackLib
Name: cracklib
Version: 2.8.18
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://cracklib.sourceforge.net
Source0: http://iweb.dl.sourceforge.net/project/cracklib/cracklib/2.8.18/cracklib-2.8.18.tar.gz
Source1: http://iweb.dl.sourceforge.net/project/cracklib/cracklib-words/2008-05-07/cracklib-words-20080507.gz

Requires(post): grep
BuildRequires: digest(sha1:%{SOURCE0}) = 3c4df51b13047fd7a85ae470f568abf8a8d6f92b
BuildRequires: digest(sha1:%{SOURCE1}) = e0cea03e505e709b15b8b950d56cb493166607da
BuildRequires: zlib-devel
BuildRequires: python-devel

%description
A Next generation version of the libCrack password checking library.

%package python
Summary: %{name} modules for Python
Group: Development/Modules
Requires: %{name} = %{version}
Requires: python(abi) = 2.7

%description python
%{name} modules for python

%package devel
Summary: Files for developing with %{name}
Group: Development/Libraries
Requires: %{name} >= %{version}

%description devel
Libraries and Header files for developing with %{name}

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib} \
  --with-default-dict=/%{_lib}/cracklib/pw_dict
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
mkdir -p %{buildroot}/%{_lib}/cracklib
mv -v %{buildroot}/usr/%{_lib}/libcrack.so.2* %{buildroot}/%{_lib}
ln -v -sf ../../%{_lib}/libcrack.so.2.8.1 %{buildroot}/usr/%{_lib}/libcrack.so
install -v -m644 -D %{SOURCE1} %{buildroot}/usr/share/dict/cracklib-words.gz
gunzip -fv %{buildroot}/usr/share/dict/cracklib-words.gz
ln -svf cracklib-words %{buildroot}/usr/share/dict/words
%find_lang %{name}
%{strip}

%post
/usr/sbin/create-cracklib-dict /usr/share/dict/cracklib-words &>/dev/null

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
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.18-3
- Optimize for size

* Mon Oct 03 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.18-2
- Fix post requirements

* Sun May 08 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.18-1
- Upgrade to 2.8.18

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.16-2
- Fixes to dependencies and ambiguous postun command.

* Thu Apr 01 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.16-1
- Upgrade to 2.8.16

* Tue Sep 8 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.8.13-1
- Initial version
