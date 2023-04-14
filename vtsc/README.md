# VTSC - Vision Turn Speed Control
Uses the predicted driving path from the model to limit speed when entering
and during curves.

"It's like being driven by a teen driver..." - me

## Branch
[pfeifer-vtsc](https://github.com/pfeiferj/openpilot/tree/pfeifer-vtsc)

## Acknowledgments
* Rewrite of the [move-fast](https://github.com/move-fast/openpilot) vtsc
implementation.
* [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot) was also used as a
reference.

## Status
Alpha

Behavior seems consistent in my limited testing. Have done a rough tune of the
constants and find it to be a reasonably good experience. Still needs some
additional features such as: status in the UI, disabling when following a lead
vehicle, and disabling at low speeds.

## Comment Blocks Text
PFEIFER - VTSC

## Why two patch files?
Currently the plan is for the changes in the first patch file to be merged
upstream into openpilot. Once merged that would make the second patch the only
code needed for the VTSC implementation. If the upstream PR gets rejected I
will merge the two patch files into a single patch instead.

## Upstream PR
The first patch in this folder is in [this](https://github.com/commaai/openpilot/pull/27741) upstream PR.

## Tuning
Tuning should primarily be performed using the constants in
selfdrive/controls/lib/vision\_turn\_controller.py. Below is a description of
the constants that have the most impact on behavior. (Ordered by what I believe
to be most impactful)

TARGET\_LAT\_A:
  - This value controls the amount of acceleration to the side that is felt
  during the curve. Increasing this value will make the controller hit curves
  "harder" while decreasing it will make the controller hit the curves "softer".

TARGET\_DECEL\_TIME:
  - This value decides how quickly to decelerate to meet the target lateral
  acceleration in the curve. Ideally we would use the distance to the shapest
  point in the curve to decide the acceleration instead, but when we fit the
  curve we effectively smooth out the curve and lose the exact point the curve
  is sharpest. So detecting that point using the polynomial will consistently
  cause the controller to think the sharpest point is occuring too soon. To
  deal with this issue we set an amount of time we plan to hit the target
  velocity. This is used to then set the desired acceleration by simply
  dividing the difference in current velocity vs desired by the time. So,
  increasing this value will make the controller less aggressively try to hit
  the velocity determined from the TARGET\_LAT\_ACCEL. Lowering the value will
  make the controller more aggressively hit the target velocity. One thing to
  note about this method of determining the acceleration is that the target
  acceleration is re-calculated at each cycle based on that point in time plus
  the TARGET\_DECEL\_TIME so the time it takes to actually hit the target
  velocity does not truly equal the value placed here. It also means that we
  will nearly always end up not quite reaching the TARGET\_LAT\_A value.

FILTER\_RC:
  - The controller uses a first order filter on the output velocity to
  smooth out changes in acceleration. The FILTER\_RC value affects the "lag" of
  the filter. Higher values will create smoother changes in acceleration at the
  cost of reaching the desired acceleration later. Lower values will make the
  acceleration react more quickly to what the controller thinks it should be
  outputing at the cost of having more sudden changes in acceleration and not
  filtering out outliers in requested values as well.

TURN\_ACTIVE\_LIMIT:
  - This value decides what curves the controller thinks it should be active
  for. Largely this affects three things. First, it uses the
  MAX\_ACTIVE\_TURN\_ACCEL to prevent too much unnecessary acceleration if the
  controllers sees another curve in the near future. Second, it prevents
  uncomfortable changes in acceleration when the future predictions move past
  the current curve while we are still experiencing moderate lateral
  acceleration. Third, it changes when we decide we are exiting a curve and can
  return to normal acceleration/velocities, thereby acting as a sort of
  deadzone on the TARGET\_LAT\_ACCEL to prevent oscillation between
  deceleration and acceleration.

EVAL\_START and EVAL\_STOP:
  - The period of time in the future predictions to check for curvature during.
  Lowering the EVAL\_STOP value may increase accuracy at the cost of making the
  controller react to upcoming curves later. Note that the mpc path values are
  only calculated for the upcoming 10 seconds, so a value larger than that will
  likely not be useful.
