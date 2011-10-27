Summary: GNU Streams Editor
Name: sed
Version: 4.2.1
Release: 3
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.gnu.org/software/sed
Source0: http://ftp.gnu.org/gnu/sed/sed-4.2.1.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = ace93d23eabc00d3a8187ecf07d3a02b1b297810

%description
Sed is used to filter text and perform modifications on it.

%prep
%setup -q

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --bindir=/bin
make %{PMFLAGS}

%install
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/usr/share/info/dir
%find_lang %{name}
%{compress_man}
%{strip}

%post
/usr/bin/install-info /usr/share/info/sed.info /usr/share/info/dir

%preun
/usr/bin/install-info --delete /usr/share/info/sed.info /usr/share/info/dir

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
/bin/sed
/usr/share/info/sed.info
/usr/share/man/man1/sed.1.bz2

%changelog
* Wed Oct 26 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-3
- Optimize sed for size

* Fri Oct 30 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-2
- Use FHS compatible info directories

* Sat Jul 25 2009 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 4.2.1-1
- Initial version
