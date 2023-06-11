# VTSC - Vision Turn Speed Control
Uses the predicted driving path from the model to limit speed when entering and
during curves.

"It's like being driven by a teen driver..." - me

## Branch
[pfeifer-vtsc](https://github.com/pfeiferj/openpilot/tree/pfeifer-vtsc)
--
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-vtsc)

## Acknowledgments
* Rewrite of the [move-fast](https://github.com/move-fast/openpilot) vtsc
implementation.
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot) was also used as a
reference.

## Status
Alpha

* Behavior is reasonably consistent, but may be possible to improve the
  consistency some by adding the mpc data to the polyfit, needs further
  investigation.

* At the moment the wheel angle is not used to track the current curve so it can
  lose track of the current curve and start to accelerate while in the curve.

* Disables based on lead detection, however this should probably be behind a
  toggle. It should also probably check the distance of the lead and only
  disable if we're close to the follow distance.

## Comment Blocks Text
PFEIFER - VTSC

## Tuning
Tuning should primarily be performed using the constants in
selfdrive/controls/lib/vision\_turn\_controller.py. Below is a description of
the constants that have the most impact on behavior. (Ordered by what I believe
to be most impactful)

TARGET\_LAT\_A:
  - This value controls the amount of acceleration to the side that is felt
    during the curve. Increasing this value will make the controller hit curves
    "harder" while decreasing it will make the controller hit the curves
    "softer".

MAX\_JERK:
  - Jerk is the rate of change of acceleration. Essentially this value limits
    how quickly the requested acceleration can change. This can keep false
    positives from harshly hitting the brakes and can help smooth out the decel
    for a curve. This value can cause overshoot of the lateral acceleration if
    the max decel value described below below is hit.


MAX\_DECEL:
  - The maximum rate at which the controller will request to slow down. Prevents
    heavy braking but will cause overshoot of the lateral acceleration when this
    limits the deceleration.
