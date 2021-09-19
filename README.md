# Mere Linux

Mere Linux is a simple Linux distribution built upon
[musl](http://www.musl-libc.org/) libc, using
[pacman](https://www.archlinux.org/pacman/) for package management and
[s6](http://skarnet.org/software/s6/) for PID 1 and process supervision.
The main system toolchain and comiler is [llvm/clang](https://llvm.org/).

Mere is still in its Alpha phase. If you are interested in helping to
shape its direction, please visit the
[Github Discussions](https://github.com/jhuntwork/merelinux/discussions/58)
page and leave a comment.

For additional details, visit [https://merelinux.org](https://merelinux.org).

## Installing

See [INSTALLING](INSTALLING.md) for more details.

## Docker Containers

There are two main docker containers that may make a good introduction to
Mere Linux.

- `mere/base`: Essentially just `busybox` and `pacman`. Use it to get going and install
any other available packages. Just 4.35 MB!
- `mere/dev`: Quite a bit larger, but that's because it includes the `llvm` toolchain and other dependencies required to begin building packages for Mere. In fact, it's the container used in the official Mere build automation.

## Support

For bugs or feature requests, including packages that do not currently exist in
the repositories, please create a
[new Github issue](https://github.com/jhuntwork/merelinux/issues).

Feel free to ask questions in the `#merelinux` channel on the
[LiberaChat IRC Network](https://libera.chat).

## Contributing

In the current state of development, the most helpful contributions are:

- Test Mere on your local machine and
  [report any issues](https://github.com/jhuntwork/merelinux/issues).
- Create pull requests of any missing packages you would like to see included.
  There is currently a lot of room for potential packages.
  See [CONTRIBUTING](CONTRIBUTING.md) for more details.
