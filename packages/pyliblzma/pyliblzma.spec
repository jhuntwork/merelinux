Summary: PylibLZMA
Name: pyliblzma
Version: 0.5.3
Release: 2
Group: System Environment/Libraries
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://launchpad.net/pyliblzma
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 6240ec6f830f35f4087b8926a95c2074320b7ed5
BuildRequires: Python-devel
BuildRequires: setuptools
BuildRequires: xz-devel

%description
PylibLZMA provides a python interface for the liblzma library to read and write
data that has been compressed or can be decompressed by Lasse Collin's XZ Utils.

%prep
%setup -q

%build
python setup.py build

%install
python setup.py install --root %{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/lib/python2.7/site-packages/*

%changelog
* Sun Jan 30 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.5.3-2
- Rebuild against xz-5.0.1

* Tue Aug 31 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.5.3-1
- Initial version
