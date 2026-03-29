# `extra`

`extra` is for packages that do not belong in `core` or `desktop`. It is the
broad general-purpose repo for the rest of the system, including common
development tooling, libraries, runtimes, and utilities.

## Inclusion

In general, `extra` is for packages that are one or more of:

- development tools and language toolchains that are not part of `core`
- general-purpose command-line utilities
- libraries that are not fundamental to the base system and are not
  primarily part of the desktop stack
- runtimes, interpreters, and supporting packages for broader application
  and developer use

## Exclusion

`extra` is intentionally broad, but it is still not a dumping ground for
packages that clearly belong in `core` or `desktop`.
