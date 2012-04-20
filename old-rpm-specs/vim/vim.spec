Summary: vim
Name: vim
Version: 7.3
Release: 1
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
PDIR=/tmp/vim-patches
SDIR=`pwd`
install -d $PDIR
cd $PDIR
wget -q -O MD5SUMS ftp://ftp.vim.org/pub/vim/patches/%{version}/MD5SUMS
IFS='
'
for line in `cat MD5SUMS` ; do
   sum=`echo $line | cut -d' ' -f1`
   file=`echo $line | cut -d' ' -f3`
   if ! echo "$sum  $file" | md5sum -c - ; then
      wget -c ftp://ftp.vim.org/pub/vim/patches/%{version}/$file
   fi
done
md5sum -c MD5SUMS
cd $SDIR
for file in $PDIR/%{version}.* ; do
   patch -p0 < $file
done
echo '#define SYS_VIMRC_FILE "/etc/vimrc"' >> src/feature.h

%build
export CFLAGS='-Os -pipe -D_GNU_SOURCE'
export LDFLAGS='--static'
./configure \
  --prefix='' \
  --enable-multibyte
make -C src auto/osdef.h
sed -i '/define stack_t/d' src/auto/config.h
sed -i '/setenv/d' src/auto/osdef.h
sed -i '/putenv/d' src/auto/osdef.h
make %{PMFLAGS}
#make test >test.out 2>&1

%install
make DESTDIR=%{buildroot} install
# Remove the following sample script due to dependency on /bin/csh
rm -v %{buildroot}/share/vim/vim73/tools/vim132
sed -i 's@/usr/bin/env@/bin/env@g' `grep -lr /usr/bin/env %{buildroot}`
find %{buildroot}/share/man -mindepth 0 -maxdepth 1 ! -name "man*" -exec rm -rf '{}' +
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
/bin/ex
/bin/rview
/bin/rvim
/bin/view
/bin/vim
/bin/vimdiff
/bin/vimtutor
/bin/xxd
/share/man/man1/*.bz2
/share/vim

%changelog
* Thu Apr 19 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 7.3-1
- Initial version
