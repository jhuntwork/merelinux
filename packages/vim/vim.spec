Summary: vim
Name: vim
Version: 7.3
Release: 1
Group: Text Editors
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.vim.org
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 46faa96c5fab639899b1c655c23d8755b62f036f
BuildRequires: ncurses-devel

%description
Vim is an advanced text editor that seeks to provide the power of the de-facto
Unix editor 'Vi', with a more complete feature set.

%prep
%setup -q -n %{name}73

%build
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --enable-multibyte
make %{PMFLAGS}
make test >test.out 2>&1

%install
make DESTDIR=%{buildroot} install
# Remove the following sample script due to dependency on /bin/csh
rm -v %{buildroot}/usr/share/vim/vim73/tools/vim132
ln -sv vim %{buildroot}/usr/bin/vi
for L in  %{buildroot}/usr/share/man/{,*/}man1/vim.1; do
    ln -sv vim.1 $(dirname $L)/vi.1
done
%{compress_man}
install -dv %{buildroot}/etc
cat > %{buildroot}/etc/vimrc << "EOF"
" Begin /etc/vimrc

set nocompatible
set backspace=2
set ruler
syntax on

" End /etc/vimrc
EOF

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%config /etc/vimrc
/usr/bin/ex
/usr/bin/rview
/usr/bin/rvim
/usr/bin/vi
/usr/bin/view
/usr/bin/vim
/usr/bin/vimdiff
/usr/bin/vimtutor
/usr/bin/xxd
/usr/share/man/man1/*
/usr/share/man/*/man1/*
/usr/share/vim

%changelog
* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.3-1
- Upgrade to 7.3

* Sat Apr 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.2-1
- Initial version
