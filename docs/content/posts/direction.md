---
title: "Direction"
date: 2021-03-13T09:40:06-05:00
draft: false
---

Up to now, development in Mere has focused on laying out its foundation.
Much of that was discovering what Mere _is_, what makes it different. At times
that has led to indecision, and that slows progress.

In the meantime, some of the ideas and chosen tools have sparked interest. But
Mere's usability has been low, as ideas and concepts took priority in
development over usability. So now, to build some adoption, the project is
re-focusing efforts to release a stable and usable first version.

To achieve this, some specific stated decisions may disappear in favor of
general usability. For now, one core principle will guide any design decisions:
Simplicity.

## Simplicity

Simplicity can mean many different things. And achieving it is usually not easy.
But as a high level goal, where possible Mere will choose tools, code,
configuration, language and documentation that is straight-forward and easy to
understand.

Sometimes that will mean the code and tools themselves are already simple. Other
times that may mean choosing to install more complex tools in a way that is
easier to use and understand. And still other times that may mean leaving out
certain features or tools to avoid complexity.

## Next Steps

So what are the specific next steps?

- Release the current core set of packages as defined in the master branch
  from the testing repository to the stable one.
- Release new docker images to match these new, stable packages.
- Update the linux kernel package to produce a generally usable, modular kernel
  supporting various hardware.
- Provide a basic, bootable installation image and tool for installing on
  hardware.
- Work on a lightweight desktop implementation guided by the goal of simplicity.

If you have ideas about the above, or interest in contributing, please visit the
[Discussions](https://github.com/jhuntwork/merelinux/discussions/58) page on
Github and say hello.
