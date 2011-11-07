Summary: vim
Name: vim
Version: 7.3
Release: 2
Group: Text Editors
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://www.vim.org
Source0: ftp://ftp.vim.org/pub/vim/unix/vim-7.3.tar.bz2

BuildRequires: digest(sha1:%{SOURCE0}) = 46faa96c5fab639899b1c655c23d8755b62f036f
BuildRequires: ncurses-devel
BuildRequires: wget

%description
Vim is an advanced text editor that seeks to provide the power of the de-facto
Unix editor 'Vi', with a more complete feature set.

%prep
%setup -q -n %{name}73
# Apply upstream patches
mkdir patches
cd patches
wget ftp://ftp.vim.org/pub/vim/patches/7.3/MD5SUMS
wget ftp://ftp.vim.org/pub/vim/patches/7.3/7.3.*
md5sum -c MD5SUMS
cd ..
for file in patches/7.3.* ; do
   patch -p0 < $file
done
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
export CFLAGS='-Os -pipe'
./configure \
  --prefix=/usr \
  --enable-multibyte
make %{PMFLAGS}
#make test >test.out 2>&1

%install
make DESTDIR=%{buildroot} install
# Remove the following sample script due to dependency on /bin/csh
rm -v %{buildroot}/usr/share/vim/vim73/tools/vim132
ln -sv vim %{buildroot}/usr/bin/vi
for L in  %{buildroot}/usr/share/man/{,*/}man1/vim.1; do
    ln -sv vim.1 $(dirname $L)/vi.1
done
%{compress_man}
%{strip}
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
/usr/share/man/man1/*.bz2
/usr/share/man/*/man1/*.bz2
/usr/share/vim

%changelog
* Mon Nov 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.3-2
- Apply all upstream patches
- Optimize for size

* Sat May 07 2011 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.3-1
- Upgrade to 7.3

* Sat Apr 10 2010 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.2-1
- Initial version
