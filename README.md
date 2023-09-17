# POP - Pfeifer Openpilot Patches
A collection of patch sets of common unsupported/unofficial community features.

## Not a developer? Read this!
This repo is primarily intended for developers. If you're not a developer you
may be better served by some of the amazing community forks of openpilot. The
following are some popular forks I am personally aware of:
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot) -
  [Discord](https://discord.gg/RB9UFGTHTZ)
    - Supports all upstream cars with a focus on HKG.
* [Twilsonco's Fork](https://github.com/twilsonco/openpilot) -
  [Discord](https://discord.com/channels/469524606043160576/884811574773157949)
    - Improved torque control for most cars supported by sunnypilot.
* [Alexandre Sato's Fork](https://github.com/AlexandreSato/openpilot/tree/personal3)
    - Primary focus on Toyota/Lexus.
* [OPKR](https://github.com/openpilotkr/openpilot) -
  [Discord](https://discord.gg/pppFp2pVW3)
    - Primary focus on HKG and Comma 2 support.
* [Dragonpilot](https://github.com/dragonpilot-community/dragonpilot)
    - Supports all upstream cars with a primary focus on Toyota and secondary
    attention to Honda and HKG.
* [Frogpilot](https://github.com/FrogAi/FrogPilot)
    - Primary focus on Toyota/Lexus and staying up to date with openpilot
      master.
* [OPGM](https://github.com/opgm/openpilot) - 
  [Discord](https://discord.com/channels/771493367246094347/978055164160266300)
    - Primary focus on adding support and qol improvements for GM vehicles.

Still want to use something in this repo? Read on about the dragons...

## WARNING! Here be dragons!
This fork and branch is intended to provide patches that add common
unsupported/unofficial community features of openpilot. Other branches in this
repo will frequently have their commit history reset in order to maintain few
commit patches. The branches are not meant to be built off of directly. Many
branches in this repo will be unstable, in particular the "pfeifer" branch
should never be expected to be in a working state. If a patch doesn't work with
the latest openpilot master please create an issue. That being said, use at your
own risk. The patches may at any time become incompatible with Openpilot master.

## Discord
Join the [discord](https://discord.gg/yqwxTAuxpN) server for discussion about
this repository and the patches.

## LICENSE
The patches are bound by the MIT License located in the
[LICENSE](./LICENSE) file of this repo and branch. The MIT License is
considered a permissive license in that it exlicitly allows you to "use,
copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software". This license does not require you to open source the
code these patches are used in or even modifications to the patches. I
have explicitly chosen a permissive license as I feel like the code
should truly be free and you should do whatever you want with the code
within the terms of the license. Also note that the commaai/openpilot
project itself uses the MIT License.

## Reading the patch docs and code
Each patch has its own folder with a readme. The readme contains details
regarding that particular patch set. In general the readme documents will
describe what the patch does, what repos were used as references when writing
the patch, the stability of the patch, the branch used for creating the patch,
and warnings regarding any known issues or other things I deem important to warn
about. Note that the readme docs are only loosely following the same pattern so
you should read the entire doc for a patch you plan to use.

### Planned for upstream
If the patch is intended for upstream I will note the upstream PR related to the
patch in the readme. Note that any patch planned for upstream will not contain
comment blocks/fences for changes

### Comment blocks/fences
If the patch is not intended for a pr to upstream then the code will contain
comments surrounding any new code. These blocks make it easier to see what
changes were for what functionality when using multiple patches. This in turn
helps with resolving any conflicts between patches. Many of the patches will
likely conflict in the params and ui sections due to the toggles and params
being placed in the same location, but the patches may have conflicts elsewhere
that would need to be resolved when using multiple patches.

### Commented out upstream code
Anywhere that lines of existing upstream code have to be replaced I comment out
the upstream code and then directly follow the commented out code with the
comment block and patch code. Generally commented out code is considered to be
an anti-pattern since your source control keeps track of the old code. I'm
commenting out code despite this for convenience. In this case the code may
frequently have conflicts with upstream changes and while resolving those
conflicts I am using the commented out code for context on what my change was vs
what has changed since then in upstream. Doing this is especially relevent since
I am rewriting my git history frequently which may cause the context to be lost.

## Utility Libraries
While many of the patches could be written to be completely standalone I've gone
the route of creating some utility libraries that patches in this repo may
depend on. These utility libraries are designed to reduce code duplication and
conflicts in the patches. Patches that require the utility libraries will
include the library commits in their combined patch file.

## Branches
### pfeifer-full branch
The pfeifer-full branch is intended to be a _somewhat_ stable branch that
combines most of the patches in the pfeifer-openpilot-patches branch. If using
multiple of the patches you may find it more convenient to cherry-pick off of
the pfeifer-full branch instead of using the patches directly because conflicts
between patches will already be resolved. Note that the git history on the
pfeifer-full branch (and most other branches) will be rewritten frequently.

### pfeifer-\*-dev branches
Any branch with -dev on the end of the name has a fairly high chance of breaking
at any time. These branches are intended for testing a change in isolation
before creating a patch.

### pfeifer branch
_DO NOT TRUST THE pfeifer BRANCH!_ As mentioned in the warning section, the
pfeifer branch is _extremely_ likely to be broken at any point in time. The
branch is used as a playground and is frequently pushed to without _any_
testing. I highly recommend you do not use this branch. It _will_ have half
baked changes. It _will_ have issues building from time to time. It _will_ have
unexpected behavior and things that are not entirely safe without full
understanding of what the possible problems of the particular changes are. It
_will_ cause crashes on openpilot from time to time that prevent openpilot from
operating.

### \*-tmp branches
_DO NOT TRUST -tmp BRANCHES!_ The above note about the pfeifer branch applies
here as well.

## Notes folder
The notes folder doesn't contain any patches, but instead it contains notes
related to openpilot. It is more or less just a collection of things that I
either needed to lookup to gain better understanding of what openpilot is doing,
or that I think would be helpful in general.
