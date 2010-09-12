Summary: Ruby Programming Language
Name: ruby
Version: 1.8.7
Release: 1
Group: Development/Languages
License: Ruby License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.ruby-lang.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}-p302.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = d93bd2f1099f3473b496cda2422b27a8da2beb00
BuildRequires: zlib-devel
BuildRequires: openssl-devel

%description
Ruby is a dynamic, open source programming language with a focus on simplicity
and productivity.

%package devel
Summary: The libraries and header files needed for ruby extension development.
Requires: %{name} = %{version}
Group: Development/Libraries

%description devel
The libraries and header files needed for ruby extension development.

%prep
%setup -q -n %{name}-%{version}-p302

%build
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --libdir=/usr/%{_lib}
make

%install
make DESTDIR=%{buildroot} install
find %{buildroot}/usr/share/man -type f -exec bzip2 -9 '{}' \;

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/ruby
/usr/bin/erb
/usr/bin/irb
/usr/bin/rdoc
/usr/bin/ri
/usr/bin/testrb
/usr/%{_lib}/ruby
/usr/share/man/man1/ruby.1.bz2

%files devel
%defattr(-,root,root)
/usr/%{_lib}/libruby-static.a

%changelog
* Sat Sep 04 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.8.7
- Initial version
