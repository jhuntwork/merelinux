# Mere Linux Recipes

This repository contains the package recipes that define Mere Linux.

Mere Linux is a musl-based Linux distribution built around the `mere`
package manager and build system. Its goal is to produce a complete system,
with a package set that spans core userspace, development tooling,
server software, and a modern desktop stack.

Mere has a distinct personality. Its center of gravity is
[musl](http://www.musl-libc.org/) rather than glibc,
[s6 and skarnet](http://skarnet.org/software/s6/) rather than systemd, and
[LLVM/Clang](https://llvm.org/) rather than a GNU-first toolchain. It favors
a lean system made from smaller, more replaceable parts wherever that is
practical.

## Repository Status

Mere Linux is currently in transition between two recipe formats:

- `legacy-packages/` contains the older `PKGBUILD`-based package
  definitions.
- New recipes are being developed in KDL format for the newer `mere`
  tooling.
