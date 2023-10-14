# VTSC - Vision Turn Speed Control
Calculates a velocity to meet a target lateral accel using curvature rates from
the model.

"It's like being driven by a teen driver..." - me

## Branch
[pfeifer-vtsc](https://github.com/pfeiferj/openpilot/tree/pfeifer-vtsc)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-vtsc)

## Acknowledgments
* Rewrite of the [move-fast](https://github.com/move-fast/openpilot) vtsc
implementation.
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot) was also used as a
reference.

## Status
Beta

[Changelog](./CHANGELOG.md)

* Overall it consistently detects and sets a good speed for curves when the
model sees them. In general if a curve is easily visible it can handle curves
with a drop in speed of up to around 20 mph.

## Comment Blocks Text
PFEIFER - VTSC

## Tuning
Tuning should primarily be performed using the constants in
selfdrive/controls/lib/vision\_turn\_controller.py.

TARGET\_LAT\_A:
- This value controls the amount of acceleration to the side that is felt
during the curve. Increasing this value will make the controller hit curves
"harder" while decreasing it will make the controller hit the curves
"softer".

MIN\_TARGET\_V:
- This is the minimum velocity the controller can request. Raising the limit may
be desirable if using experimental mode at low speeds.

