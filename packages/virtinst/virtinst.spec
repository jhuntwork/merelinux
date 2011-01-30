Summary: The Virt Install tool
Name: virtinst
Version: 0.500.5
Release: 1
Group: Development/Languages
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
URL: http://virt-manager.et.redhat.com
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

Requires: urlgrabber
Requires: libvirt-python
Requires: libxml2-python
BuildRequires: digest(sha1:%{SOURCE0}) = 42555de065d4391d3c6043e971d0bb8ff457d19a
BuildRequires: Python-devel

%description
The "Virt Install" tool is a command line tool which provides an easy way to
provision operating systems into virtual machines. It also provides an API to
the virt-manager application for its graphical VM creation wizard.

%prep
%setup -q

%build
export LDFLAGS="%{LDFLAGS}"
python ./setup.py build

%install
python ./setup.py install --root=%{buildroot}
%{find_lang} %{name}
%{compress_man}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/usr/bin/virt-clone
/usr/bin/virt-convert
/usr/bin/virt-image
/usr/bin/virt-install
/usr/lib/python2.7/site-packages/virtinst
/usr/lib/python2.7/site-packages/virtconv
/usr/lib/python2.7/site-packages/virtinst-%{version}-py2.7.egg-info
/usr/share/man/man1/virt-clone.1.bz2
/usr/share/man/man1/virt-convert.1.bz2
/usr/share/man/man1/virt-image.1.bz2
/usr/share/man/man1/virt-install.1.bz2
/usr/share/man/man5/virt-image.5.bz2

%changelog
* Sat Jan 29 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.500.5-1
- Initial version
