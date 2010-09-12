Summary: mongoDB
Name: mongodb
Version: 1.6.2
Release: 1
Group: Services
License: AGPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mongodb.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-src-r%{version}.tar.gz
Source1: http://dev.lightcube.us/sources/%{name}/mongod.init

BuildRequires: digest(sha1:%{SOURCE0}) = 0a7ef4825a6ec6f91a272611fde7c0b46eacd89a
BuildRequires: digest(sha1:%{SOURCE1}) = 497cd02f1f2a4577bc06819eaee5f43306981e34
BuildRequires: boost-devel
BuildRequires: scons
BuildRequires: pcre-devel
BuildRequires: js-devel
BuildRequires: readline-devel
BuildRequires: ncurses-devel
BuildRequires: libpcap-devel

%description
MongoDB (from "humongous") is a scalable, high-performance, open source,
document-oriented database

%prep
%setup -q -n %{name}-src-r%{version}

%build
scons all

%install
scons --prefix=%{buildroot}/usr install
install -dv %{buildroot}/etc/init.d
install -v -m0754 %{SOURCE1} %{buildroot}/etc/init.d/mongod
install -dv %{buildroot}/usr/sbin
install -dv %{buildroot}/srv/mongodb
mv -v %{buildroot}/usr/bin/mongod %{buildroot}/usr/sbin/
cat > %{buildroot}/etc/mongod.conf << "EOF"
dbpath = /srv/mongodb
logpath = /var/log/mongodb.log
fork = true
auth = true
EOF

%preun
/usr/sbin/remove_initd mongod || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/mongod.conf
/etc/init.d/mongod
/usr/bin/bsondump
/usr/bin/mongo
/usr/bin/mongodump
/usr/bin/mongoexport
/usr/bin/mongofiles
/usr/bin/mongoimport
/usr/bin/mongorestore
/usr/bin/mongos
/usr/bin/mongosniff
/usr/bin/mongostat
/usr/sbin/mongod
%dir /srv/mongodb

%changelog
* Sun Sep 12 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.2-1
- Upgrade to 1.6.2

* Sun Aug 22 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.1-1
- Upgrade to 1.6.1

* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.0-1
- Initial version
