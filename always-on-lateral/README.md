# Always On Lateral
An always on lateral implementation that allows keeping lateral controls on
after hitting the brake or pressing the cancel button. To engage you must
activate cruise control after turning the main cruise button on. To disengage
toggle the main cruise control off. Can be configured to only remain active when
pressing the cruise cancel button and disable completely when the brake is
pressed. Can also be configured to disable when blinkers are activated.

## comma.ai requirements for panda safety modifications
This change requires changes to panda safety. If you make modifications to panda
safety comma.ai states that you should not use the openpilot branding for your
fork. This means your fork should not be named "openpilot". You can still use
the installer.comma.ai installer by having your repo be previously named
openpilot and then changing it to your own branded name.

Note that there are two levels of changes to panda safety. The first level is
any change that modifies it has the above branding requirements. The second
level is that any change that comma.ai deems outright unsafe will result in
devices that are uploading logs with those changes will be banned from comma
services. comma.ai suggested reading and following the following iso guidelines
to maintain the safety of your users:
[iso-15622](https://www.iso.org/obp/ui/en/#iso:std:iso:15622:ed-3:v1:en),
[iso-11270](https://www.iso.org/obp/ui/en/#iso:std:iso:11270:ed-1:v1:en).
However, despite that recommendation from comma.ai it's worth noting that they
have the right to ban a device for any reason and will do so if they see a
change that they deem to be dangerous even if it follows the iso guidelines.

This code does to the best of my knowledge meet the requirements to not be
banned from comma.ai services and is reasonably safe to use. However, there is
always some risk associated to modifying panda in any way and I have not tested
these changes on all cars. If you use this code you are using it at your own
risk and the risk of anyone who installs your software. I suggest you take a
look at the changes these patches make before using and make sure you understand
the change. The change does not make modifications to the controls allowed state
of the longitudinal controls, so all longitudinal behavior should remain the
same.

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
* Chrysler (Thanks @Shaggy!)
* Honda (Thanks @sapander!)

### Reported Issues
GM:
* disables lateral while applying regen braking with paddle. Lateral resumes
after releasing the paddle. (Thanks @Mangomoose)

### Untested Cars
The following cars _may_ be supported, but they have not been verified working.
Test them at your own risk and offroad before using them onroad. If you do
verify an implementation is working please create an issue for me to move it to
the supported cars list. If you find any issues please create an issue
describing the undesired behavior.

* Ford
* Mazda
* Nissan
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

## Comment Blocks Text
PFEIFER - AOL


## Using
This change requires two patches due to it modifying both openpilot and panda.
Please read the panda safety section of this README before using the patches.
Applying the openpilot patch will point the panda module in the openpilot repo
to my commit hash. I recommend that you apply the panda patch to your own panda
repo and then create another commit overwriting the commit hash in the openpilot
repo to your own panda with always on lateral. I may rewrite the git history on
my always on lateral branch at any time.
