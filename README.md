# Mere Linux Recipes

This repository contains the package recipes that define Mere Linux.

Mere Linux is a musl-based Linux distribution built around the
[mere](https://codeberg.org/merelinux/mere) package manager and build system.
Its goal is to produce a complete system, with a package set that spans core
userspace, development tooling, server software, and a modern desktop stack.

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

## Repository Layout

Package recipes live under `repos/<repo-name>/<package-name>/recipe.kdl`

Each package directory is the complete home for that package recipe. Local
patches, config files, and other bundled sources should live beside
`recipe.kdl` in the same package directory.

Each package should belong to one repo based on its role in the system. While
an overview is provided below, each individual repo directory will define its
own more specific inclusion rules.

### Current Repos

#### core

`core` is for the small set of packages that are fundamental to installing,
building, managing, and repairing a Mere Linux system. More details can be
found in [`repos/core/README.md`](repos/core/README.md).

#### desktop

`desktop` is for packages that primarily exist to provide a graphical
desktop environment, graphical desktop applications, or the supporting stack
they depend on in Mere. More details can be found in
[`repos/desktop/README.md`](repos/desktop/README.md).

#### extra

`extra` is for packages that do not belong in `core` or `desktop`. It is the
broad general-purpose repo for the rest of the system, including common
development tooling, libraries, runtimes, and utilities. More details can be
found in [`repos/extra/README.md`](repos/extra/README.md).
