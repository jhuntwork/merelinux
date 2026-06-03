# Contributing Recipes

Thanks for your interest in contributing to Mere Linux!

## What you'll need

- The `mere` binary ([download](https://codeberg.org/merelinux/mere/releases/latest))
- An initialized store (`sudo mere store init`)
- The official repo config and key:
  ```sh
  sudo curl -so /mere/config.kdl https://pkgs.merelinux.org/config.kdl
  sudo curl -so /mere/keys/mere.pub https://pkgs.merelinux.org/mere.pub
  ```

## Writing a recipe

Recipes live at `recipes/<category>/<package-name>/recipe.kdl`.

For the full format reference, see the
[Recipe Specification](https://codeberg.org/merelinux/mere/src/branch/main/docs/design/recipe_spec.md).

A minimal recipe looks like:

```kdl
recipe {
    name "mypackage"
    version "1.0.0"
    release 1
    description "Short description"
    url "https://upstream.example.com"
    licenses "MIT"
    archs "aarch64" "x86_64"
    depends "busybox" "llvm" "musl-dev"
}

source "https://example.com/mypackage-${recipe.version}.tar.gz" {
    blake3 "<hash>"
}

build {
    script r#"
        make
    "#
}

install {
    script r#"
        make DESTDIR="$DESTDIR" install
    "#
}

package "mypackage" {
    files "usr/bin/" \
          "usr/lib/"
}
```

## Computing the source hash

```sh
mere dev hash /path/to/downloaded-source.tar.gz
```

This prints the BLAKE3 hash to use in your recipe's `source` block.

## Validating without building

```sh
mere dev validate recipes/<category>/<package-name>/recipe.kdl
```

Checks the recipe syntax and structure without running a build.

## Building locally

```sh
mere dev build recipes/<category>/<package-name>/recipe.kdl
```

This downloads sources, verifies hashes, builds in an isolated namespace,
and produces `.pkg.tar.zst` archives in `/mere/dev/outputs/`.

Use `-v` for verbose output if something fails.

## Testing your built packages

### Set up a signing key (first time only)

```sh
mere dev key generate
```

This generates a local Ed25519 key pair for signing dev packages.
The key is stored at `~/.mere/keys/mere.key` by default.

### Import to a local repo

```sh
mere dev import local
```

This signs and imports all built packages from `/mere/dev/outputs/` into a
local development repository at `/mere/dev/repo/local/`. You can use any
name in place of `local`.

### Install and test

Create a profile and install your package into it:

```sh
mere profile create test
mere install -p test mypackage
```

Then try it out in an isolated shell:

```sh
mere shell -p test
mypackage --version
```

This drops you into a shell with only your profile's packages available.
Type `exit` to return to your host environment.

## Submitting

1. Fork this repository
2. Create a branch for your recipe
3. Ensure `mere dev build` succeeds for your recipe
4. Open a pull request with a brief description of the package

## Tips

- Look at existing recipes in `recipes/` for patterns
- Build dependencies go in the `depends` field and are installed into the
  build profile automatically
- Use `${recipe.version}` and `${recipe.name}` in source URLs for consistency
- Split packages (e.g. `-dev`) use multiple `package` blocks with different
  `files` patterns
- If your build needs `cmake`, `meson`, `ninja`, etc., add them to `depends`
