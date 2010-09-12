Summary: Postfix MTA
Name: postfix
Version: 2.7.1
Release: 1
Group: Services
License: IBM Public License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.postfix.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz
Source1: http://dev.lightcube.us/sources/%{name}/%{name}.init

BuildRequires: digest(%{SOURCE0}) = b7a5c3ccd309156a65d6f8d2683d4fa1
BuildRequires: digest(%{SOURCE1}) = 6b5839cdeaa91b671134e60f41c4e24d
BuildRequires: db-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: zlib-devel
BuildRequires: cyrus-sasl-devel

%description
Postfix is Wietse Venema's mailer that started life at IBM research as an
alternative to the widely-used Sendmail program.
Postfix attempts to be fast, easy to administer, and secure. The outside has
a definite Sendmail-ish flavor, but the inside is completely different.

%prep
%setup -q

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
make makefiles \
     CCARGS='%{CFLAGS} -DDEF_DAEMON_DIR=\"/usr/lib/postfix\" -DUSE_SASL_AUTH -DUSE_CYRUS_SASL -DDEF_MANPAGE_DIR=\"/usr/share/man\" -DHAS_PCRE -DUSE_TLS -I/usr/include/sasl/ -I/usr/include/openssl/' \
     AUXLIBS='-L/usr/%{_lib} -lsasl2 -lpcre -ldb -lz -lm -lssl -lcrypto %{LDFLAGS}'
make

%install
sh postfix-install -non-interactive install_root=%{buildroot}
install -dv %{buildroot}/etc/init.d
install -m754 %{SOURCE1} %{buildroot}/etc/init.d/%{name}
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%post
/usr/sbin/install_initd postfix

%preun
/usr/sbin/remove_initd postfix || /bin/true

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%dir /etc/postfix
%config /etc/postfix/main.cf
%config /etc/postfix/master.cf
/etc/postfix/LICENSE
/etc/postfix/TLS_LICENSE
%config /etc/postfix/access
%config /etc/postfix/aliases
/etc/postfix/bounce.cf.default
%config /etc/postfix/canonical
%config /etc/postfix/generic
%config /etc/postfix/header_checks
/etc/postfix/main.cf.default
/etc/postfix/makedefs.out
%config /etc/postfix/relocated
%config /etc/postfix/transport
%config /etc/postfix/virtual
/etc/init.d/postfix
/usr/bin/mailq
/usr/bin/newaliases
/usr/lib/postfix
/usr/sbin/postalias
/usr/sbin/postcat
/usr/sbin/postconf
/usr/sbin/postfix
/usr/sbin/postkick
/usr/sbin/postlock
/usr/sbin/postlog
/usr/sbin/postmap
/usr/sbin/postmulti
/usr/sbin/postsuper
/usr/sbin/sendmail
/usr/share/man/man1/*
/usr/share/man/man5/*
/usr/share/man/man8/*
%dir /var/spool/postfix
%defattr(-,postfix,postfix)
/var/spool/postfix/active
/var/spool/postfix/bounce
/var/spool/postfix/corrupt
/var/spool/postfix/defer
/var/spool/postfix/deferred
/var/spool/postfix/flush
/var/spool/postfix/hold
/var/spool/postfix/incoming
/var/spool/postfix/private
/var/spool/postfix/saved
/var/spool/postfix/trace
%defattr(-,postfix,postdrop)
/var/spool/postfix/public
/var/spool/postfix/maildrop
%defattr(2755,root,postdrop)
/usr/sbin/postdrop
/usr/sbin/postqueue

%changelog
* Tue Aug 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 2.7.1-1
- Initial version
