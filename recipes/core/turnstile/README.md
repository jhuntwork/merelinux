# Turnstile integration

Installation does not enable the service or add `pam_turnstile.so` to login
policies. Integrate genuine login entry points explicitly; changing the shared
`system-session` stack also affects su/sudo. Do not include that login-tracking
stack in Turnstile's internal `/etc/pam.d/turnstiled`: it can recurse.

The optional dinit backend needs Mere's dinit and BusyBox utilities. Programs
called from its shell script are not all inferred package dependencies. The
recipe adjusts the backend's monitor path to `/bin/dinit-monitor`.

`readiness-fd.patch` lets Mere gate dependent services on the listening control
socket using `TURNSTILED_READY_FD` and `ready-notification`. Login managers should
depend on `turnstiled`, not assume process startup means readiness.

**Do not restart or stop Turnstile during active sessions:** it removes managed
runtime directories even while PAM callers remain alive; sessions are not
transparently reattached after restart.

## Isolated tests

After building the recipe:

```sh
sudo python test/turnstile/session-lifecycle.py \
    /mere/dev/build/turnstile-0.1.11-1-<workspace-id>/pkg/turnstile
```

Requires root, Python, mount/PID namespaces, dinit/BusyBox tools under `/bin`,
and the package's runtime libraries/PAM modules on the host. Tests use a
disposable chroot, not host PAM or runtime directories. They cover readiness,
PAM lifecycle, concurrent logins, basic path safety, and the optional dinit
user-service backend. Negative tests intentionally log errors.

The dinit fixture uses a stub sysinit; full boot ordering, cgroups, lingering,
real desktop services and aarch64 remain unverified. For greetd integration,
see [its recipe notes](../../desktop/greetd/README.md).
