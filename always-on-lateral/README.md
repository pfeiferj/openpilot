# Always On Lateral
An always on lateral implementation that allows keeping lateral controls on
after hitting the brake or pressing the cancel button. To engage you must
activate cruise control after turning the main cruise button on. To disengage
toggle the main cruise control off. Can be configured to only remain active when
pressing the cruise cancel button and disable completely when the brake is
pressed. Can also be configured to disable when blinkers are activated.

## Cars Supported
I have only personally tested an HKG can vehicle.

### Reported Working Cars
The following cars were reported working by members of the community:
* HKG can-fd (Thanks @hoomoose!)
* Toyota (Thanks @FrogAi!)
* GM (Thanks [@OPGM Community!](https://discord.gg/G2xp9AH94U))
* VW (Thanks [@Frogpilot Community!](https://l.linklyhq.com/l/1t3Il))
    - Note: frogpilot implementation is _slightly_ different but uses same panda
    code so YYMV

### Untested Cars
The following cars _may_ be supported, but they have not been verified working.
Test them at your own risk and offroad before using them onroad. If you do
verify an implementation is working please create an issue for me to move it to
the supported cars list. If you find any issues please create an issue
describing the undesired behavior.

* Chrysler
* Ford
* Honda
* Mazda
* Subaru
* Tesla
* VW/Audi/Skoda

## Branch
* Openpilot: [pfeifer-always-on-lateral](https://github.com/pfeiferj/openpilot/tree/pfeifer-always-on-lateral)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-always-on-lateral)

* Panda: [pfeifer-always-on-lateral](https://github.com/pfeiferj/panda/tree/pfeifer-always-on-lateral)
\-
[diff](https://github.com/commaai/panda/compare/master...pfeiferj:panda:pfeifer-always-on-lateral)

## Acknowledgments
I used the following forks as references:
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot)
* [Spektor56's Ghostpilot](https://github.com/spektor56/ghostpilot)
* [Alexandre Sato's Fork](https://github.com/AlexandreSato/openpilot/tree/personal3)

## Status
Beta

[Changelog](./CHANGELOG.md)

* Many cars are untested. However, results so far suggest that remaining untested cars are likely to work.
* Missing Nissan support

## Comment Blocks Text
PFEIFER - AOL

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
repo to your own panda with always on lateral. I may rewrite the git history on
my always on lateral branch at any time.
