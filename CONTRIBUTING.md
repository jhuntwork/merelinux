# Contributing to Mere Linux

## Package Development

### What should I know before I start?

Mere Linux uses [pacman](https://archlinux.org/pacman/) as its package manager,
with some customizations. Each package has its own directory under the
[packages](packages/) directory, which contains at least a
[PKGBUILD](https://archlinux.org/pacman/PKGBUILD.5.html) file.

Some `PKGBUILD` files may create multiple, related packages, called 'split packages'.
A typical example would be a package that provides a run-time library and a
corresponding `-dev` package that provides library headers, development documentation,
static libraries, or other components required for using the library at build-time.

While packages can be built using only the `makepkg` utility provided with the
`pacman-build` package, Mere's build utilities are designed around building inside
a Docker container. This helps achieve isolation and an easily repeatable
environment when building a package, resulting in fewer build issues. This also
has the advantage of detaching a build host system from the build requirements.
For example, it is easy to create a Mere package on a MacOS system running Docker
Desktop by simply using the same build utilities.

### Creating a New Package

1. Create a new directory under [packages](packages/)
2. Copy [template.PKGBUILD](template.PKGBUILD) to `packages/<newpkg>/PKGBUILD`.
3. Edit the new `PKGBUILD` file, adjusting the `pkgname`, `pkgver`,
   `pkgdesc`. `url` and `license` variables. You may also need to adjust the
   `sources` variable to match the full url of your source archive, and
   `makedepends` if your package has additional build-time dependencies.
4. Adjust the `build` and `package` functions as necessary to correctly compile
   and install the package contents. (For examples of more advanced
   configurations, see the [musl](packages/musl/PKGBUILD) or
   [s6](packages/s6/PKGBUILD) `PKGBUILD` files.)
5. Run: `./buildpkg.sh packages/<newpkg>` to launch the build script inside a
   Docker container. This will create temporary directories in your package
   directory called `pkg` and `src`. You can inspect those after the build
   script and container has exited to see what has been produced. Or, if you
   prefer to develop inside the container interactively, you can run
   `./buildpkg.sh packages/<newpkg> sh` instead, which will give you a shell
   prompt inside the build environment container.
