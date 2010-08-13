Summary: mongoDB
Name: mongodb
Version: 1.6.0
Release: 1
Group: Services
License: AGPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.mongodb.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-src-r%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/%{name}/mongod-init.sh

Requires: base-layout, glibc, pcre, js, readline, ncurses, libpcap
BuildRequires: digest(%{SOURCE0}) = d09e062b518ce71106652eac0e88a962
BuildRequires: boost-devel, scons, pcre-devel, js-devel, readline-devel, ncurses-devel, libpcap-devel

%description
MongoDB (from "humongous") is a scalable, high-performance, open source,
document-oriented database

%prep
%setup -q -n %{name}-src-r%{version}

%build
scons all

%install
scons --prefix=%{buildroot}/usr install
install -dv %{buildroot}/etc/rc.d/init.d
install -v -m0755 %{SOURCE1} %{buildroot}/etc/rc.d/init.d/mongod
install -dv %{buildroot}/usr/sbin
install -dv %{buildroot}/srv/mongodb
mv -v %{buildroot}/usr/bin/mongod %{buildroot}/usr/sbin/
cat > %{buildroot}/etc/mongod.conf << "EOF"
dbpath = /srv/mongodb
logpath = /var/log/mongodb.log
fork = true
auth = true
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/mongod.conf
/etc/rc.d/init.d/mongod
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
/srv/mongodb

%changelog
* Wed Aug 11 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.6.0-1
- Initial version
