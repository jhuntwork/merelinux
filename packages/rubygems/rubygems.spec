Summary: RubyGems
Name: rubygems
Version: 1.3.7
Release: 1
Group: Development/Languages
License: Ruby License
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://rubygems.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tgz
BuildArch: noarch

BuildRequires: digest(sha1:%{SOURCE0}) = 68ad2970963db9893b76acc8777be72a77c4bee4
BuildRequires: ruby

%description
RubyGems is a package management framework for Ruby.

%prep
%setup -q

%build

%install
ruby setup.rb --destdir=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/usr/bin/gem
/usr/%{_lib}/ruby/site_ruby/1.8/*

%changelog
* Sat Sep 04 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 1.3.7
- Initial version
