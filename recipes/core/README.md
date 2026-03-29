# core

`core` is the tightest and most conservative repo in the recipes tree.

## Inclusion

In general, `core` is for packages that are one or more of:

- required for base system installation
- required to build the `mere` package manager itself
- required for boot, init, or essential system administration
- required often enough in recovery or bootstrap scenarios that the system
  becomes materially worse without them

## Exclusion

`core` should stay small on purpose. A package does not belong in `core`
just because it is common, useful, or low-level. If there is doubt, prefer
keeping it out until a stronger case exists.
