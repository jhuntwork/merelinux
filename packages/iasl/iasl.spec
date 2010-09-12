Summary: iASL compiler
Name: iasl
Version: 20100806
Release: 1
Group: Development/Tools
License: Intel
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://acpica.org
Source0: http://dev.lightcube.us/sources/acpica/acpica-unix-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 92637084cbb3357db422eab25a00a1937896276f

%description
Intel ACPI Source Language compiler

%prep
%setup -q -n acpica-unix-%{version}

%build
cd compiler
CFLAGS="%{CFLAGS}" LDFLAGS="%{LDFLAGS}" make

%install
install -dv %{buildroot}/usr/bin
install -m0755 compiler/iasl %{buildroot}/usr/bin/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/iasl

%changelog
* Thu Sep 09 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 20100806-1
- Initial version
