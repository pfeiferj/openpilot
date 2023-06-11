# MADS
Modified Assistive Driving with Safety (aka Always On Lateral)

A simple mads implementation that enables always on lateral with the ability to
toggle disengage lateral on brakes as well as disengage lateral on blinker.

## Cars Supported
Currently only supports hkg-can vehicles but more will likely be added.

## Branch
* Openpilot: [pfeifer-mads](https://github.com/pfeiferj/openpilot/tree/pfeifer-mads)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-mads)

* Panda: [pfeifer-mads](https://github.com/pfeiferj/panda/tree/pfeifer-mads)
\-
[diff](https://github.com/commaai/panda/compare/master...pfeiferj:openpilot:pfeifer-mads)

## Acknowledgments
I used the following forks as references:
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot)
* [Spektor56's Ghostpilot](https://github.com/spektor56/ghostpilot)
* [Alexandre Sato's Fork](https://github.com/AlexandreSato/openpilot/tree/personal3)

## Status
Alpha

[Changelog](./CHANGELOG.md)

* Some additional testing of keeping sync with panda may be needed.
* Limited car support.
* There may need to be a restart of the ignition if the always on later toggle is enabled, needs further investigation.

## Comment Blocks Text
PFEIFER - mads

## Panda Safety
This code does to the best of my knowledge meet the panda safety standards.
However, there is always some risk associated to modifying panda in any way. I
suggest you take a look at the changes these patches make before using and
make sure you understand the change. The change does not make modifications
to the controls allowed state of the longitudinal controls, so all longitudinal
behavior should remain the same.

## Using
This change requires two patches due to it modifying both openpilot and panda.
Please read the panda safety section of this README before using the patches.
Applying the openpilot patch will point the panda module in the openpilot repo
to my commit hash. I recommend that you apply the panda patch to your own panda
repo and then create another commit overwriting the commit hash in the openpilot
repo to your own panda with mads. I may rewrite the git history on my mads branch
at any time.
