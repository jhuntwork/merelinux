Summary: Fontconfig is a library for configuring and customizing font access. 
Name: fontconfig
Version: 2.8.0
Release: 1
Group: System Environment/Base
License: GPLv2
Distribution: LightCube OS
Vendor: LightCube Solutions
URL: http://freetype.sourceforge.net/index2.html
Source0: http://dev.lightcube.us/sources/%{name}/%{name}-%{version}.tar.gz

BuildRequires: digest(sha1:%{SOURCE0}) = 570fb55eb14f2c92a7b470b941e9d35dbfafa716
BuildRequires: freetype-devel
BuildRequires: libxml2-devel

%description
Fontconfig automatically discovers new fonts when installed, performs font name
substitution, identifies the set of fonts required to completely cover a set of
languages, efficiently finds the fonts you need among the set of fonts you have
installed, and can be used in concert with the X Render Extension and FreeType
to implement high quality, anti-aliased and subpixel rendered text on a display.

%package devel
Summary: Libraries and headers for developing with libfontconfig
Group: Development/Libraries
Requires: %{name} >= %{version}
%description devel
Libraries and headers for developing with libfontconfig

%package doc
Summary: Documentation for fontconfig
Group: Development/Documentation
Requires: %{name} >= %{version}
%description doc
Documentation for fontconfig

%prep
%setup -q

%build
./configure --prefix=/usr --sysconfdir=/etc --libdir=/usr/%{_lib} \
  --localstatedir=/var --disable-silent-rules --enable-libxml2
make

%install
make DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/etc/fonts
/usr/%{_lib}/libfontconfig.so.1.4.4
/usr/%{_lib}/libfontconfig.so.1
/usr/bin/fc-cache
/usr/bin/fc-cat
/usr/bin/fc-list
/usr/bin/fc-match
/usr/bin/fc-query
/usr/bin/fc-scan
/var/cache/fontconfig
/usr/share/man/man1/fc-cache.1
/usr/share/man/man1/fc-cat.1
/usr/share/man/man1/fc-list.1
/usr/share/man/man1/fc-match.1
/usr/share/man/man1/fc-query.1
/usr/share/man/man1/fc-scan.1
/usr/share/man/man5/fonts-conf.5

%files devel
%defattr(-,root,root)
/usr/include/fontconfig
/usr/%{_lib}/libfontconfig.so
/usr/%{_lib}/libfontconfig.la
/usr/%{_lib}/libfontconfig.a
/usr/%{_lib}/pkgconfig/fontconfig.pc
/usr/share/man/man3/FcAtomicCreate.3
/usr/share/man/man3/FcAtomicLock.3
/usr/share/man/man3/FcAtomicNewFile.3
/usr/share/man/man3/FcAtomicOrigFile.3
/usr/share/man/man3/FcAtomicReplaceOrig.3
/usr/share/man/man3/FcAtomicDeleteNew.3
/usr/share/man/man3/FcAtomicUnlock.3
/usr/share/man/man3/FcAtomicDestroy.3
/usr/share/man/man3/FcBlanksCreate.3
/usr/share/man/man3/FcBlanksDestroy.3
/usr/share/man/man3/FcBlanksAdd.3
/usr/share/man/man3/FcBlanksIsMember.3
/usr/share/man/man3/FcCacheDir.3
/usr/share/man/man3/FcCacheCopySet.3
/usr/share/man/man3/FcCacheSubdir.3
/usr/share/man/man3/FcCacheNumSubdir.3
/usr/share/man/man3/FcCacheNumFont.3
/usr/share/man/man3/FcCharSetCreate.3
/usr/share/man/man3/FcCharSetDestroy.3
/usr/share/man/man3/FcCharSetAddChar.3
/usr/share/man/man3/FcCharSetCopy.3
/usr/share/man/man3/FcCharSetEqual.3
/usr/share/man/man3/FcCharSetIntersect.3
/usr/share/man/man3/FcCharSetUnion.3
/usr/share/man/man3/FcCharSetSubtract.3
/usr/share/man/man3/FcCharSetMerge.3
/usr/share/man/man3/FcCharSetHasChar.3
/usr/share/man/man3/FcCharSetCount.3
/usr/share/man/man3/FcCharSetIntersectCount.3
/usr/share/man/man3/FcCharSetSubtractCount.3
/usr/share/man/man3/FcCharSetIsSubset.3
/usr/share/man/man3/FcCharSetFirstPage.3
/usr/share/man/man3/FcCharSetNextPage.3
/usr/share/man/man3/FcCharSetCoverage.3
/usr/share/man/man3/FcCharSetNew.3
/usr/share/man/man3/FcConfigCreate.3
/usr/share/man/man3/FcConfigReference.3
/usr/share/man/man3/FcConfigDestroy.3
/usr/share/man/man3/FcConfigSetCurrent.3
/usr/share/man/man3/FcConfigGetCurrent.3
/usr/share/man/man3/FcConfigUptoDate.3
/usr/share/man/man3/FcConfigHome.3
/usr/share/man/man3/FcConfigEnableHome.3
/usr/share/man/man3/FcConfigBuildFonts.3
/usr/share/man/man3/FcConfigGetConfigDirs.3
/usr/share/man/man3/FcConfigGetFontDirs.3
/usr/share/man/man3/FcConfigGetConfigFiles.3
/usr/share/man/man3/FcConfigGetCache.3
/usr/share/man/man3/FcConfigGetCacheDirs.3
/usr/share/man/man3/FcConfigGetFonts.3
/usr/share/man/man3/FcConfigGetBlanks.3
/usr/share/man/man3/FcConfigGetRescanInterval.3
/usr/share/man/man3/FcConfigSetRescanInterval.3
/usr/share/man/man3/FcConfigAppFontAddFile.3
/usr/share/man/man3/FcConfigAppFontAddDir.3
/usr/share/man/man3/FcConfigAppFontClear.3
/usr/share/man/man3/FcConfigSubstituteWithPat.3
/usr/share/man/man3/FcConfigSubstitute.3
/usr/share/man/man3/FcFontMatch.3
/usr/share/man/man3/FcFontSort.3
/usr/share/man/man3/FcFontRenderPrepare.3
/usr/share/man/man3/FcFontList.3
/usr/share/man/man3/FcConfigFilename.3
/usr/share/man/man3/FcConfigParseAndLoad.3
/usr/share/man/man3/FcNameRegisterConstants.3
/usr/share/man/man3/FcNameUnregisterConstants.3
/usr/share/man/man3/FcNameGetConstant.3
/usr/share/man/man3/FcNameConstant.3
/usr/share/man/man3/FcDirCacheUnlink.3
/usr/share/man/man3/FcDirCacheValid.3
/usr/share/man/man3/FcDirCacheLoad.3
/usr/share/man/man3/FcDirCacheRead.3
/usr/share/man/man3/FcDirCacheLoadFile.3
/usr/share/man/man3/FcDirCacheUnload.3
/usr/share/man/man3/FcFileScan.3
/usr/share/man/man3/FcFileIsDir.3
/usr/share/man/man3/FcDirScan.3
/usr/share/man/man3/FcDirSave.3
/usr/share/man/man3/FcFontSetCreate.3
/usr/share/man/man3/FcFontSetDestroy.3
/usr/share/man/man3/FcFontSetAdd.3
/usr/share/man/man3/FcFontSetList.3
/usr/share/man/man3/FcFontSetMatch.3
/usr/share/man/man3/FcFontSetPrint.3
/usr/share/man/man3/FcFontSetSort.3
/usr/share/man/man3/FcFontSetSortDestroy.3
/usr/share/man/man3/FcPatternFormat.3
/usr/share/man/man3/FcFreeTypeCharIndex.3
/usr/share/man/man3/FcFreeTypeCharSet.3
/usr/share/man/man3/FcFreeTypeCharSetAndSpacing.3
/usr/share/man/man3/FcFreeTypeQuery.3
/usr/share/man/man3/FcFreeTypeQueryFace.3
/usr/share/man/man3/FcInitLoadConfig.3
/usr/share/man/man3/FcInitLoadConfigAndFonts.3
/usr/share/man/man3/FcInit.3
/usr/share/man/man3/FcFini.3
/usr/share/man/man3/FcGetVersion.3
/usr/share/man/man3/FcInitReinitialize.3
/usr/share/man/man3/FcInitBringUptoDate.3
/usr/share/man/man3/FcLangSetCreate.3
/usr/share/man/man3/FcLangSetDestroy.3
/usr/share/man/man3/FcLangSetCopy.3
/usr/share/man/man3/FcLangSetAdd.3
/usr/share/man/man3/FcLangSetCompare.3
/usr/share/man/man3/FcLangSetContains.3
/usr/share/man/man3/FcLangSetEqual.3
/usr/share/man/man3/FcLangSetHash.3
/usr/share/man/man3/FcLangSetHasLang.3
/usr/share/man/man3/FcLangSetGetLangs.3
/usr/share/man/man3/FcGetLangs.3
/usr/share/man/man3/FcLangGetCharSet.3
/usr/share/man/man3/FcMatrixInit.3
/usr/share/man/man3/FcMatrixCopy.3
/usr/share/man/man3/FcMatrixEqual.3
/usr/share/man/man3/FcMatrixMultiply.3
/usr/share/man/man3/FcMatrixRotate.3
/usr/share/man/man3/FcMatrixScale.3
/usr/share/man/man3/FcMatrixShear.3
/usr/share/man/man3/FcObjectSetCreate.3
/usr/share/man/man3/FcObjectSetAdd.3
/usr/share/man/man3/FcObjectSetDestroy.3
/usr/share/man/man3/FcObjectSetBuild.3
/usr/share/man/man3/FcNameRegisterObjectTypes.3
/usr/share/man/man3/FcNameUnregisterObjectTypes.3
/usr/share/man/man3/FcNameParse.3
/usr/share/man/man3/FcNameGetObjectType.3
/usr/share/man/man3/FcPatternCreate.3
/usr/share/man/man3/FcPatternDuplicate.3
/usr/share/man/man3/FcPatternReference.3
/usr/share/man/man3/FcPatternDestroy.3
/usr/share/man/man3/FcPatternEqual.3
/usr/share/man/man3/FcPatternEqualSubset.3
/usr/share/man/man3/FcPatternFilter.3
/usr/share/man/man3/FcPatternHash.3
/usr/share/man/man3/FcPatternAdd.3
/usr/share/man/man3/FcPatternAddWeak.3
/usr/share/man/man3/FcPatternAdd-Type.3
/usr/share/man/man3/FcPatternGet.3
/usr/share/man/man3/FcPatternGet-Type.3
/usr/share/man/man3/FcPatternBuild.3
/usr/share/man/man3/FcPatternDel.3
/usr/share/man/man3/FcPatternRemove.3
/usr/share/man/man3/FcPatternPrint.3
/usr/share/man/man3/FcDefaultSubstitute.3
/usr/share/man/man3/FcNameUnparse.3
/usr/share/man/man3/FcUtf8ToUcs4.3
/usr/share/man/man3/FcUcs4ToUtf8.3
/usr/share/man/man3/FcUtf8Len.3
/usr/share/man/man3/FcUtf16ToUcs4.3
/usr/share/man/man3/FcUtf16Len.3
/usr/share/man/man3/FcIsLower.3
/usr/share/man/man3/FcIsUpper.3
/usr/share/man/man3/FcToLower.3
/usr/share/man/man3/FcStrCopy.3
/usr/share/man/man3/FcStrDowncase.3
/usr/share/man/man3/FcStrCopyFilename.3
/usr/share/man/man3/FcStrCmp.3
/usr/share/man/man3/FcStrCmpIgnoreCase.3
/usr/share/man/man3/FcStrStr.3
/usr/share/man/man3/FcStrStrIgnoreCase.3
/usr/share/man/man3/FcStrPlus.3
/usr/share/man/man3/FcStrFree.3
/usr/share/man/man3/FcStrDirname.3
/usr/share/man/man3/FcStrBasename.3
/usr/share/man/man3/FcStrSetCreate.3
/usr/share/man/man3/FcStrSetMember.3
/usr/share/man/man3/FcStrSetEqual.3
/usr/share/man/man3/FcStrSetAdd.3
/usr/share/man/man3/FcStrSetAddFilename.3
/usr/share/man/man3/FcStrSetDel.3
/usr/share/man/man3/FcStrSetDestroy.3
/usr/share/man/man3/FcStrListCreate.3
/usr/share/man/man3/FcStrListNext.3
/usr/share/man/man3/FcStrListDone.3
/usr/share/man/man3/FcValueDestroy.3
/usr/share/man/man3/FcValueSave.3
/usr/share/man/man3/FcValuePrint.3
/usr/share/man/man3/FcValueEqual.3

%files doc
%defattr(-,root,root)
/usr/share/doc/fontconfig

%changelog
* Wed May 11 2011 Archaic <lc@diatribe.org>
- Initial version
