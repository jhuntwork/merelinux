# `desktop`

`desktop` is for packages that primarily exist to provide a graphical
desktop environment, graphical desktop applications, or the supporting stack
they depend on in Mere.

## Inclusion

In general, `desktop` is for packages that are one or more of:

- graphical desktop applications
- window managers, compositors, panels, launchers, and related desktop
  session components
- display, input, graphics, media, and toolkit libraries that primarily
  exist to support the desktop stack in Mere
- packages that are not intrinsically graphical upstream, but are used in
  Mere primarily as part of the desktop environment

## Exclusion

`desktop` is not for packages just because they can be used on a desktop
system. If a package is general-purpose and not primarily part of the
graphical stack in Mere, it should usually live elsewhere.
