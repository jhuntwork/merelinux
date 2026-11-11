# greetd integration

Install Turnstile alongside greetd. Mere's inferred dependencies capture linked
PAM libraries, not the dynamically loaded `pam_turnstile.so` module. The generated
service depends on Turnstile's readiness and stops before Turnstile at shutdown.
See [Turnstile's session-lifecycle caveats](../../core/turnstile/README.md).

## Provisioning

Account creation is not automatic. Provision a locked, unprivileged `greeter`
account with a home, for example:

```sh
sudo useradd --system --user-group --create-home --home-dir /var/lib/greetd \
    --shell /bin/false greeter
```

Do not set a password or run the greeter as root. Reserve VT7 before enabling
greetd and preserve an independent console/recovery login. Installing this
package does not enable it or change shared console/su/sudo PAM policy.

To launch River/Meander through agreety, select
`agreety --cmd /usr/bin/meander-session` after installing its dependencies.
Graphical integration must ensure seatd startup ordering and user access. A
graphical greeter additionally needs seat access for its own account. Do not
set a global `XDG_RUNTIME_DIR`; PAM supplies separate per-UID directories.

## Validation

The recipe runs workspace binary/library unit tests, not doctests: Mere's
current Rust package lacks rustdoc. `fail-on-runtime-error.patch` corrects
upstream's zero exit status on errors such as a missing greeter account.

After building both recipes:

```sh
sudo python test/greetd/session-integration.py \
    /mere/dev/build/greetd-0.10.3-1-<workspace-id>/pkg/greetd \
    /mere/dev/build/turnstile-0.1.11-1-<workspace-id>/pkg/turnstile
```

Requires the Turnstile test prerequisites, Python 3.11+, libcrypt and linux-pam's
`unix_chkpwd` helper. The suite tests real PAM authentication and greetd IPC in
isolation, using disposable accounts, dummy session commands and `vt = none`.
It never touches host VTs or login configuration. Interactive agreety, physical
VT switching, graphical sessions, full boot behavior and aarch64 remain untested.
