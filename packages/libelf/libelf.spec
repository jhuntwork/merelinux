Summary: elfutils libelf
Name: libelf
Version: 0.152
Release: 1
Group: Development/Utilities
License: GPL
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: https://fedorahosted.org/elfutils
#Source0: https://fedorahosted.org/releases/e/l/elfutils/0.152/elfutils-0.152.tar.bz2
Source0: http://dev.lightcube.us/sources/elfutils/elfutils-0.152.tar.bz2
Patch0: elfutils-portability.patch
Patch1: elfutils-add_ar.h.patch

BuildRequires: digest(sha1:%{SOURCE0}) = b22380205ed3ad5145586b4074be190057eb2537
BuildRequires: digest(sha1:%{PATCH0})  = c989fa702fd473f01d4af1261ad39b02b889a305
BuildRequires: digest(sha1:%{PATCH1})  = edc29acfa394639ffbfd1d8ad2c25932a3b52151
BuildRequires: zlib-devel
#BuildRequires: bzip2-devel
#BuildRequires: xz-devel

%description
Provides utilites for processing ELF files in an
architecture-independent way.

%package devel
Summary: Libraries and headers for developing with libelf
Group: Development/Libraries

%description devel
Libraries and headers for developing with libelf

%prep
%setup -q -n elfutils-%{version}
%patch0 -p1
%patch1 -p1
%{config_musl}
# Swap out usage of loff_t for off_t
sed -i 's@loff_t@off_t@g' libelf/libelf.h
#add TEMP_FAILURE_RETRY macro
sed -i "/stdint/s@.*@&\n#define TEMP_FAILURE_RETRY(x) x\n#define rawmemchr(s,c) memchr((s),(size_t)-1,(c))@" lib/system.h
# no cdefs.h header
sed -i -e '/cdefs/d' -e "/define CONCAT/s@.*@#define CONCAT1(x,y) x##y\n#define CONCAT(x,y) CONCAT1(x,y)@" lib/fixedsizehash.h
sed -i -e \
      "s@__BEGIN_DECLS@#ifdef __cplusplus\nextern \"C\" {\n#endif@" \
      -e "s@__END_DECLS@#ifdef __cplusplus\n}\n#endif@" libelf/elf.h
# use mempcpy instead of __mempcpy
sed -i 's@__mempcpy@mempcpy@g' libelf/elf_begin.c 

%build
export CFLAGS="-D_GNU_SOURCE -Os"
./configure \
  --prefix='' \
  --disable-nls
find . -name Makefile -exec sed -i 's/-Werror//g' '{}' \;
make -C libelf %{PMFLAGS} libelf.a

%install
make -C libelf DESTDIR=%{buildroot} install-includeHEADERS
install -d %{buildroot}/lib
install -m644 libelf/libelf.a %{buildroot}/lib/
%{strip}

%clean
rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
/include/gelf.h
/include/libelf.h
/include/nlist.h
/lib/libelf.a

%changelog
* Mon Apr 16 2012 Jeremy Huntwork <jhuntwork@lightcubesolutions.com> - 0.152-1
- Initial version
