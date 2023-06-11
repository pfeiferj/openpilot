# HKG-can Longitudinal Tuning Improvements
Improvements to how openpilot sends longitudinal commands to allow for smoother
acceleration and deceleration while still maintaining responsiveness.

## Status
Beta

[Changelog](./CHANGELOG.md)

Longitudinal control should be noticeably smoother. Previously there were some
edge cases of unexpected behavior when stopping or rapidly accelerating. These
edge cases should be resolved but there could still be improvements made.

## Supported Cars
* HKG - can (no can-fd support yet)

## Branch
[pfeifer-hkg-long-control-tune](https://github.com/pfeiferj/openpilot/tree/pfeifer-hkg-long-control-tune)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-hkg-long-control-tune)

## Upstream
This is planned to eventually be in an upstream PR, but a past PR was rejected.

## Detailed Explanation of Change
Calculate jerk from the acceleration plan and use as the lower limit value when
sending accel commands to hyundai can vehicles.

Using small min values for the jerk increases the resolution of the acceleration
that the car provides. This allows the car to better fit the acceleration to the
plan by making smaller adjustments to the acceleration to maintain/hit the
target acceleration.

However, with too small of values for either the min or max jerk the car
responds to changes in acceleration very sluggishly. Thus when we are requesting
rapid changes to acceleration we need larger jerk values.

To achieve a good balance of resolution to responsiveness we can determine what
the jerk in the planned acceleration is between the last acc command and the
current command and use that as the basis of the values we request from the car.
This allows a dynamic resolution that matches the current demands of the plan.
