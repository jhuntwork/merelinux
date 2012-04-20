Summary: Smart Package Manager
Name: smart
Version: 1.4
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://labix.org/smart
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-r993.tar.bz2

Requires: pyliblzma, rpm-python
BuildRequires: digest(sha1:%{SOURCE0}) = d92d95515be781a024dede22ae6ee028418c4f62
BuildRequires: python-devel

%description
The Smart Package Manager project has the ambitious objective of creating smart
and portable algorithms for solving adequately the problem of managing software
upgrades and installation. This tool works in all major distributions and will
bring notable advantages over native tools currently in use (APT, APT-RPM, YUM,
URPMI, etc).

%package extras
Summary: Extra pieces that are useful but are not necessary at runtime
Group: Extras
Requires: %{name} >= %{version}

%description extras
Extra pieces that are useful but are not necessary at runtime, such as
man pages, locale messages and extra documentation

%prep
%setup -q -n %{name}-%{version}-r993
rm -rf locale

%build
make

%install
make DESTDIR=%{buildroot} install
%{compress_man}
install -dv %{buildroot}/usr/lib/smart
cat > %{buildroot}/usr/lib/smart/distro.py << "EOF"
if not sysconf.getReadOnly():
            sysconf.set("channels.lightcube", {
                            "type": "rpm-md",
                            "name": "LightCube OS Repository",
                            "baseurl": "http://dev.lightcube.us/pub/LightCubeOS/stable"
                        })
EOF
# Do not do multi downloads
sed -i '/^MAXACTIVEDOWNLOADS/s@= .*@= 1@' %{buildroot}/usr/lib/python2.7/site-packages/smart/fetcher.py
# Do not use pycurl ever
sed -i 's@import pycurl@&foobar@g' %{buildroot}/usr/lib/python2.7/site-packages/smart/fetcher.py

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/smart
/usr/lib/python2.7/site-packages/*
/usr/lib/smart

%files extras
/usr/share/man/man8/smart.8.bz2

%changelog
* Fri Feb 03 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.4-1
- Initial version
