# Mere Linux

Mere Linux is a simple Linux distribution built upon
[musl](http://www.musl-libc.org/) libc, using
[pacman](https://www.archlinux.org/pacman/) for package management and
[s6](http://skarnet.org/software/s6/) for PID 1 and process supervision.

Mere is still in its Alpha phase. If you are interested in helping to
shape its direction, please visit the
[Github Discussions](https://github.com/jhuntwork/merelinux/discussions/58)
page and leave a comment.

For additional details, visit [https://merelinux.org](https://merelinux.org).

## Installing

Currently there is no Mere-specific installation media. However, Mere can be
installed to disk manually from any x86_64 Linux system using a statically
compiled version of `pacman`. Detailed instructions are forthcoming in a
separate installation document.

## Support

Feel free to ask questions in the `#merelinux` channel on the
[LiberaChat IRC Network](https://libera.chat).

## Contributing

In the current state of development, the most helpful contributions are:

- Test Mere on your local machine and
  [report any issues](https://github.com/jhuntwork/merelinux/issues).
- Create pull requests of any missing packages you would like to see included.
  There is currently a lot of room for potential packages.
  See [CONTRIBUTING](CONTRIBUTING.md) for more details.
