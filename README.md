# POP - Pfeifer Openpilot Patches
A collection of single (or few) commit patches of common unsupported/unofficial
community features.

# Not a developer? Read this!
This repo is primarily intended for developers. If you're not a developer you
may be better served by some of the amazing community forks of openpilot. The
following are some popular forks I am personally aware of:
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot)
    - Supports all upstream cars with a focus on HKG.
* [Twilsonco's Fork](https://github.com/twilsonco/openpilot)
    - Primary focus on adding support for GM.
* [Alexandre Sato's Fork](https://github.com/AlexandreSato/openpilot/tree/personal3)
    - Primary focus on Toyota.
* [OPKR](https://github.com/openpilotkr/openpilot)
    - Primary focus on HKG and Comma 2 support.
* [Dragonpilot](https://github.com/dragonpilot-community/dragonpilot)
    - Supports all upstream cars with a primary focus on Toyota and secondary
    attention to Honda and HKG.

Still want to use something in this repo? Read on about the dragons...

# WARNING! Here be dragons!
This fork and branch is intended to provide patches that add common
unsupported/unofficial community features of openpilot. Other branches in this
repo will frequently have their commit history reset in order to maintain
single commit patches. The branches are not meant to be built off of directly.
Many branches in this repo will be unstable, in particular the "pfeifer" branch
should never be expected to be in a working state. If a patch doesn't work
with the latest openpilot master please create an issue. That being said, use
at your own risk. The patches may at any time become incompatible with Openpilot
master.
