# Speed Limit Control
Limits openpilot's speed based on the current speed limit. Supports the
following sources:
* Nav Instructions: Provided by openpilot nav instructions.
* Map: Provided by openstreetmap. (requires mapd)
* Car: Provided by some supported cars.

Priority for speed limits is in the order of the list above. So if nav
instructions are providing a speed limit and the car is also providing a speed
limit the nav instruction speed limit will be used (assuming both are enabled).

On supported cars an offset for the speed limit can be set by double pressing
the gap button. Once double pressed the offset is calculated by using the
current set max speed minus the current speed limit. For example, if the speed
limit is 55 mph and you have the maximum speed set to 60 mph the calculated
offset will be +5 mph. This means if the speed limit lowers to 45 mph openpilot
will limit the speed to 50 mph (45 mph speed limit plus 5 mph offset).

## Car Speed Limit Supported Cars
* HKG

## Double Press Gap Supported Cars
* HKG

### Double Press Gap Untested Cars
* GM
* Toyota

## Branch
[pfeifer-speed-limit-control](https://github.com/pfeiferj/openpilot/tree/pfeifer-speed-limit-control)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-speed-limit-control)


## Acknowledgments
* HKG button state was referenced from
  [Sunnypilot](https://github.com/sunnyhaibin/sunnypilot)

## Status
Alpha

## Comment Blocks Text
PFEIFER - SLC

## Dependencies
The following dependencies are included in the combined patch file:
* button-manager (Comment Block Text: PFEIFER - BM)
* gap-adjust-button (Comment Block Text: PFEIFER - GAB)
