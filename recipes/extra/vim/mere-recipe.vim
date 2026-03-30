" Vim syntax file
" Language:     Mere Linux Recipe (KDL)
" Maintainer:   Mere Linux
" Last Change:  2025-02-08
" Filenames:    recipe.kdl

if exists("b:current_syntax")
  finish
endif

" Load shell syntax for embedded script blocks
if exists("b:current_syntax")
  let s:current_syntax = b:current_syntax
  unlet b:current_syntax
endif
syn include @mereShell syntax/sh.vim
if exists("s:current_syntax")
  let b:current_syntax = s:current_syntax
endif

" Comments
syn match mereComment "//.*$" contains=mereTodo
syn region mereComment start="/\*" end="\*/" contains=mereTodo
syn keyword mereTodo TODO FIXME XXX NOTE contained

" Top-level nodes
syn keyword mereTopNode recipe vars source prepare build check install package nextgroup=mereNodeArg skipwhite

" Recipe properties
syn keyword mereRecipeProp name version release description url licenses archs depends env contained

" Source properties
syn keyword mereSourceProp blake3 contained

" Phase properties
syn keyword merePhaseProp env script contained

" Package properties
syn keyword merePackageProp files install contained

" Node arguments (strings after node name)
syn region mereNodeArg start=+"+ skip=+\\"+ end=+"+ contained contains=mereVarInterp

" Shell script blocks (with embedded shell syntax)
" Match: script r#"..."# or script "..."
syn region mereScriptRaw matchgroup=mereRawString start=+script\s\+r\z(#*\)"+ end=+"\z1+ contains=@mereShell,mereVarInterp keepend
syn region mereScriptString matchgroup=mereString start=+script\s\+"+ skip=+\\"+ end=+"+ contains=@mereShell,mereVarInterp,mereEscape keepend

" Strings (regular and raw, for non-script contexts)
syn region mereString start=+"+ skip=+\\"+ end=+"+ contains=mereVarInterp,mereEscape
syn region mereRawString start=+r\z(#*\)"+ end=+"\z1+ contains=mereVarInterp

" Escape sequences in strings
syn match mereEscape +\\[nrt"\\]+ contained

" Variable interpolation
syn match mereVarInterp "\${[^}]\+}" contained contains=mereVarPrefix,mereVarName
syn match mereVarPrefix "\${" contained
syn match mereVarName "[a-zA-Z_][a-zA-Z0-9_.-]*" contained

" Built-in recipe variables
syn keyword mereBuiltinVar recipe.name recipe.version recipe.release contained
syn keyword mereBuiltinVar vars pkgver srcdir pkgdir DESTDIR SOURCES_DIR contained
syn keyword mereBuiltinVar MERE_PKG_NAME MERE_PKG_VERSION MERE_PKG_RELEASE contained
syn keyword mereBuiltinVar MERE_PKG_ARCH MERE_BASE_PKG_NAME MERE_SUBPKG contained
syn keyword mereBuiltinVar MERE_OUTPUTS MERE_ROOT MERE_BUILD_DIR contained
syn keyword mereBuiltinVar MERE_SRC_DIR MERE_PKG_DIR MERE_STORE_DIR PREFIX contained

" Numbers
syn match mereNumber "\<\d\+\>"
syn match mereNumber "\<0x[0-9a-fA-F]\+\>"

" Booleans
syn keyword mereBoolean true false

" Properties (key=value, key "value", or key <number>)
syn match mereProp "[a-zA-Z_-]\+\ze\s*=" contains=mereRecipeProp,mereSourceProp,merePhaseProp,merePackageProp
syn match mereProp "[a-zA-Z_-]\+\ze\s\+\"" contains=mereRecipeProp,mereSourceProp,merePhaseProp,merePackageProp
syn match mereProp "[a-zA-Z_-]\+\ze\s\+\d" contains=mereRecipeProp,mereSourceProp,merePhaseProp,merePackageProp

" Operators
syn match mereOperator "="

" Braces
syn match mereBrace "[{}]"

" Architecture names
syn keyword mereArch x86_64 aarch64 armv7 i686 contained

" Common license identifiers
syn keyword mereLicense GPL GPL-2 GPL-3 MIT BSD Apache Apache-2.0 LGPL MPL ISC contained

" Highlight groups
hi def link mereComment Comment
hi def link mereTodo Todo
hi def link mereTopNode Keyword
hi def link mereRecipeProp Identifier
hi def link mereSourceProp Identifier
hi def link merePhaseProp Identifier
hi def link merePackageProp Identifier
hi def link mereNodeArg String
hi def link mereString String
hi def link mereRawString String
hi def link mereEscape SpecialChar
hi def link mereVarInterp Special
hi def link mereVarPrefix Delimiter
hi def link mereVarName Identifier
hi def link mereBuiltinVar Constant
hi def link mereNumber Number
hi def link mereBoolean Boolean
hi def link mereProp Type
hi def link mereOperator Operator
hi def link mereBrace Delimiter
hi def link mereArch Constant
hi def link mereLicense Constant

let b:current_syntax = "mere-recipe"
