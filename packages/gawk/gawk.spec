Summary: Gawk
Name: gawk
Version: 4.0.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/gawk
Source0: http://ftp.gnu.org/gnu/gawk/gawk-4.0.0.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 9e1b7d86b5e80c85e699c269d59d6711753c51d1

%description
Gawk is the GNU implementation of the awk command. The utility
interprets a special-purpose programming language that makes it
possible to handle many data-reformatting jobs with just a few
lines of code.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --libexecdir=/usr/%{_lib}
make %{PMFLAGS}
make check

%install
make DESTDIR=%{buildroot} install
install -dv %{buildroot}/bin
mv -v %{buildroot}/usr/bin/gawk %{buildroot}/bin
rm -v %{buildroot}/usr/bin/awk
ln -sv gawk %{buildroot}/bin/awk
rm -f %{buildroot}/usr/share/info/dir
%{compress_man}
%{strip}
%find_lang %{name}

%post
/usr/bin/install-info /usr/share/info/gawk.info /usr/share/info/dir
/usr/bin/install-info /usr/share/info/gawkinet.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/gawk.info /usr/share/info/dir
/usr/bin/install-info --delete /usr/share/info/gawkinet.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/awk
/bin/gawk
/usr/bin/gawk-%{version}
/usr/bin/dgawk
/usr/bin/igawk
/usr/bin/pgawk
/usr/bin/pgawk-%{version}
/usr/%{_lib}/awk
/usr/share/awk
/usr/share/info/gawk.info
/usr/share/info/gawkinet.info
/usr/share/man/man1/gawk.1.bz2
/usr/share/man/man1/igawk.1.bz2
/usr/share/man/man1/pgawk.1.bz2

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.0.0-1
- Upgrade to 4.0.0
- Optimize for size

* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.8-2
- Move gawk and awk to /bin.

* Sun Aug 08 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.8-1
- Upgrade to 3.1.8

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.7-2
- Use FHS compatible info directories

* Fri Aug 14 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 3.1.7-1
- Initial version
