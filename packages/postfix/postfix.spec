Summary: Postfix MTA
Name: postfix
Version: 2.7.1
Release: 1
Group: Services
License: IBM Public License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.postfix.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/~jhuntwork/sources/blfs-bootscripts/blfs-bootscripts-20090302.tar.bz2

Requires: base-layout, glibc, openssl, db, pcre, zlib
BuildRequires: digest(%{SOURCE0}) = b7a5c3ccd309156a65d6f8d2683d4fa1
BuildRequires: digest(%{SOURCE1}) = 7ee5363f223235adc54046623ffa77cd
BuildRequires: db-devel, openssl-devel, pcre-devel, zlib-devel

%description
Postfix is Wietse Venema's mailer that started life at IBM research as an
alternative to the widely-used Sendmail program.
Postfix attempts to be fast, easy to administer, and secure. The outside has
a definite Sendmail-ish flavor, but the inside is completely different.

%prep
%setup -q

%build
make makefiles \
     CCARGS='-DDEF_DAEMON_DIR=\"/usr/lib/postfix\" -DUSE_SASL_AUTH -DUSE_CYRUS_SASL -DDEF_MANPAGE_DIR=\"/usr/share/man\" -DHAS_PCRE -DUSE_TLS -I/usr/include/sasl/ -I/usr/include/openssl/' \
     AUXLIBS='-L/usr/%{_lib} -lsasl2 -lpcre -ldb -lz -lm -lssl -lcrypto'
make

%install
sh postfix-install -non-interactive install_root=%{buildroot}
install -dv %{buildroot}/etc/rc.d/init.d
tar -xf %{SOURCE1}
sed -i 's@^# Begin.*@&\n# chkconfig: 345 25 35\n# description: Postfix MTA@' \
  blfs-bootscripts-20090302/blfs/init.d/postfix
install -m754 blfs-bootscripts-20090302/blfs/init.d/postfix \
  %{buildroot}/etc/rc.d/init.d/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/postfix
/etc/rc.d/init.d/postfix
/usr/bin/mailq
/usr/bin/newaliases
/usr/lib/postfix
/usr/sbin/postalias
/usr/sbin/postcat
/usr/sbin/postconf
/usr/sbin/postdrop
/usr/sbin/postfix
/usr/sbin/postkick
/usr/sbin/postlock
/usr/sbin/postlog
/usr/sbin/postmap
/usr/sbin/postmulti
/usr/sbin/postqueue
/usr/sbin/postsuper
/usr/sbin/sendmail
/usr/share/man/man1/mailq.1
/usr/share/man/man1/newaliases.1
/usr/share/man/man1/postalias.1
/usr/share/man/man1/postcat.1
/usr/share/man/man1/postconf.1
/usr/share/man/man1/postdrop.1
/usr/share/man/man1/postfix.1
/usr/share/man/man1/postkick.1
/usr/share/man/man1/postlock.1
/usr/share/man/man1/postlog.1
/usr/share/man/man1/postmap.1
/usr/share/man/man1/postmulti.1
/usr/share/man/man1/postqueue.1
/usr/share/man/man1/postsuper.1
/usr/share/man/man1/sendmail.1
/usr/share/man/man5/access.5
/usr/share/man/man5/aliases.5
/usr/share/man/man5/body_checks.5
/usr/share/man/man5/bounce.5
/usr/share/man/man5/canonical.5
/usr/share/man/man5/cidr_table.5
/usr/share/man/man5/generic.5
/usr/share/man/man5/header_checks.5
/usr/share/man/man5/ldap_table.5
/usr/share/man/man5/master.5
/usr/share/man/man5/mysql_table.5
/usr/share/man/man5/nisplus_table.5
/usr/share/man/man5/pcre_table.5
/usr/share/man/man5/pgsql_table.5
/usr/share/man/man5/postconf.5
/usr/share/man/man5/postfix-wrapper.5
/usr/share/man/man5/regexp_table.5
/usr/share/man/man5/relocated.5
/usr/share/man/man5/tcp_table.5
/usr/share/man/man5/transport.5
/usr/share/man/man5/virtual.5
/usr/share/man/man8/anvil.8
/usr/share/man/man8/bounce.8
/usr/share/man/man8/cleanup.8
/usr/share/man/man8/defer.8
/usr/share/man/man8/discard.8
/usr/share/man/man8/error.8
/usr/share/man/man8/flush.8
/usr/share/man/man8/lmtp.8
/usr/share/man/man8/local.8
/usr/share/man/man8/master.8
/usr/share/man/man8/oqmgr.8
/usr/share/man/man8/pickup.8
/usr/share/man/man8/pipe.8
/usr/share/man/man8/proxymap.8
/usr/share/man/man8/qmgr.8
/usr/share/man/man8/qmqpd.8
/usr/share/man/man8/scache.8
/usr/share/man/man8/showq.8
/usr/share/man/man8/smtp.8
/usr/share/man/man8/smtpd.8
/usr/share/man/man8/spawn.8
/usr/share/man/man8/tlsmgr.8
/usr/share/man/man8/trace.8
/usr/share/man/man8/trivial-rewrite.8
/usr/share/man/man8/verify.8
/usr/share/man/man8/virtual.8

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.1-1
- Initial version
