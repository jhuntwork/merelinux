Summary: vim
Name: vim
Version: 7.2
Release: 1
Group: Text Editors
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.vim.org
Source0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}.tar.bz2
Patch0: http://dev.lightcube.us/~jhuntwork/sources/%{name}/%{name}-%{version}-fixes-5.patch

Requires: base-layout, glibc, ncurses
BuildRequires: digest(%{SOURCE0}) = f0901284b338e448bfd79ccca0041254
BuildRequires: digest(%{PATCH0}) = 3af30a47fbf94d141c4317bf87d28e25
BuildRequires: ncurses-devel

%description
Vim is an advanced text editor that seeks to provide the power of the de-facto
Unix editor 'Vi', with a more complete feature set.

%prep
%setup -q -n %{name}72
%patch0 -p1

%build
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h
export CFLAGS="%{CFLAGS}"
export LDFLAGS="%{LDFLAGS}"
./configure \
  --prefix=/usr \
  --enable-multibyte
make

%install
make DESTDIR=%{buildroot} install
# Remove the following sample script due to dependency on /bin/csh
rm -v %{buildroot}/usr/share/vim/vim72/tools/vim132
ln -sv vim %{buildroot}/usr/bin/vi
for L in  %{buildroot}/usr/share/man/{,*/}man1/vim.1; do
    ln -sv vim.1 $(dirname $L)/vi.1
done
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
/etc/vimrc
/usr/bin/ex
/usr/bin/rview
/usr/bin/rvim
/usr/bin/vi
/usr/bin/view
/usr/bin/vim
/usr/bin/vimdiff
/usr/bin/vimtutor
/usr/bin/xxd
/usr/share/man/man1/evim.1
/usr/share/man/man1/ex.1
/usr/share/man/man1/rview.1
/usr/share/man/man1/rvim.1
/usr/share/man/man1/view.1
/usr/share/man/man1/vi.1
/usr/share/man/man1/vim.1
/usr/share/man/man1/vimdiff.1
/usr/share/man/man1/vimtutor.1
/usr/share/man/man1/xxd.1
/usr/share/man/*/man1/evim.1
/usr/share/man/*/man1/ex.1
/usr/share/man/*/man1/rview.1
/usr/share/man/*/man1/rvim.1
/usr/share/man/*/man1/view.1
/usr/share/man/*/man1/vi.1
/usr/share/man/*/man1/vim.1
/usr/share/man/*/man1/vimdiff.1
/usr/share/man/*/man1/vimtutor.1
/usr/share/man/*/man1/xxd.1
/usr/share/vim

%changelog
* Sat Apr 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.2-1
- Initial version
