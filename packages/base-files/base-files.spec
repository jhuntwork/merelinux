Summary: Essential System Files
Name: base-files
Version: 0.1
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
Buildarch: noarch
Source0: https://dev.lightcube.us/svn/lightcubeos/!svn/bc/430/lightcube_os/trunk/packages/%{name}/passwd
Source1: https://dev.lightcube.us/svn/lightcubeos/!svn/bc/430/lightcube_os/trunk/packages/%{name}/group
Source2: https://dev.lightcube.us/svn/lightcubeos/!svn/bc/430/lightcube_os/trunk/packages/%{name}/inputrc

Requires: base-layout
BuildRequires: digest(sha1:%{SOURCE0}) = a05e76d0256fb4c9428e3ab101c6a5d80caf54a1
BuildRequires: digest(sha1:%{SOURCE1}) = 0cfa6426123620ba6d19777d7461891568e9e4f0
BuildRequires: digest(sha1:%{SOURCE2}) = b5b083ef90b918b68c67b7c54f37c91e46b5b706

%description
Provides core files needed by the base system.

%prep
%setup -T -c

%install
install -dv %{buildroot}/{etc,dev,var}
install -dv %{buildroot}/var/{run,log}
install -dv %{buildroot}/{dev,etc,var}
install -dv %{buildroot}/var/{log,run}
install -m0644 %{SOURCE0} %{buildroot}/etc/passwd
install -m0644 %{SOURCE1} %{buildroot}/etc/group
install -m0644 %{SOURCE2} %{buildroot}/etc/inputrc

# The following is only for upgrading between 0.1-2 and 0.1-3
# Remove the full %pre and %post on next upgrade
%pre
mv /var/log/lastlog /tmp/lastlog &>/dev/null || /bin/true
mv /var/log/wtmp /tmp/wtmp &>/dev/null || /bin/true
mv /var/log/btmp /tmp/btmp &>/dev/null || /bin/true
mv /var/run/utmp /tmp/utmp &>/dev/null || /bin/true

%post
mv /tmp/lastlog /var/log/lastlog &>/dev/null || /bin/true
mv /tmp/wtmp /var/log/wtmp &>/dev/null || /bin/true
mv /tmp/btmp /var/log/btmp &>/dev/null || /bin/true
mv /tmp/utmp /var/run/utmp &>/dev/null || /bin/true
/bin/mknod -m 600 /dev/console c 5 1 &>/dev/null || /bin/true
/bin/mknod -m 666 /dev/null c 1 3 &>/dev/null || /bin/true
cat /proc/mounts >/etc/mtab

%files
%defattr(-,root,root)
%config /etc/passwd
%config /etc/group
%config /etc/inputrc

%changelog
* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-3
- Don't package mtab, wtmp, btmp, utmp, lastlog or dev/{console,null}

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-2
- Add nginx user and group.

* Mon Apr 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.1-1
- Add inputrc file. Increment local version.

* Sat Jul 18 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.0-1
- Initial version
