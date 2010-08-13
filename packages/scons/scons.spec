Summary: SCons - a Software Construction tool
Name: scons
Version: 1.3.1
Release: 1
Group: Development/Tools
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.scons.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz

Requires: base-layout, glibc, Python
BuildRequires: digest(%{SOURCE0}) = e3411dc316b2f6be5226cd71dbdeb0c1

%description
SCons is a software construction tool (build tool, substitute for Make)
implemented in Python, based on the winning design in the Software Carpentry
build tool competition (in turn based on the Cons build tool).

%prep
%setup -q

%build

%install
python setup.py install --prefix=%{buildroot}/usr --standard-lib
mkdir -v %{buildroot}/usr/share
mv %{buildroot}/usr/man %{buildroot}/usr/share/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/scons
/usr/bin/scons-1.3.1
/usr/bin/scons-time
/usr/bin/scons-time-1.3.1
/usr/bin/sconsign
/usr/bin/sconsign-1.3.1
/usr/lib/python2.7/site-packages/SCons
/usr/lib/python2.7/site-packages/scons-1.3.1-py2.7.egg-info
/usr/share/man/man1/scons-time.1
/usr/share/man/man1/scons.1
/usr/share/man/man1/sconsign.1

%changelog
* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.1-1
- Initial version
