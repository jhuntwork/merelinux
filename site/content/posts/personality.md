---
title: "Personality"
date: 2021-04-11T13:03:51-04:00
draft: false
---

Like many things, Mere Linux has a sort of personality. Various
decisions have molded its shape, its structure, its feel. Simplicity was
already mentioned in the [Direction]({{< ref "direction.md" >}}) post. Here are
a couple more.

## No Systemd

Mere Linux does not and will not use systemd. There's many reasons why, but the
most fundamental one is that it breaks the principle of Simplicity. The author
of the excellent s6 suite of packages
[says it well](https://skarnet.org/software/systemd.html):

> The single, overarching problem with systemd is that it attempts, in every
> possible way, to do *more* instead of *less*.

The author of musl has also written some compelling
[technical arguments against systemd](https://ewontfix.com/14/).

Instead, Mere Linux uses s6 for init and will continue to do so for the
foreseeable future. The article
[Why another supervision suite ?](https://skarnet.org/software/s6/why.html)
highlights the benefits and implications of this choice.

## Mere Linux is not GNU/Linux

Mere does use some GNU software, but it's not anywhere near a majority, or even
a large part of the core system. At the time of this writing, searching
`PKGBUILD` files for references to "gnu.org" turns up 16 hits, out of 73
packages. That's not quite 22% and most of those are development
tools that may not even be present on some systems. A minimal installation of
Mere Linux as a web server would likely have 0 GNU packages installed.

While Mere doesn't completely rule out using GNU software, it will steer away
from it where reasonable. One reason why is because GNU tends to add its own
features and extensions to standard tools. Due to wide adoption, many people
end up developing around that, expecting its presence. This leads to a lot of
non-portable tooling and unexpected breakage where there doesn't need to be.

Another reason is that much of GNU's stated purpose is political idealism that
Mere as a project does not attach itself to. Mere licenses its own internal
tools under a permissive MIT license and does not aim to advance any political
ideals.
