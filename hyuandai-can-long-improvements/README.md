# HKG-can Longitudinal Control Improvements
Improvements to how openpilot sends longitudinal commands to allow for smoother
acceleration and deceleration while still maintaining responsiveness.

# Status
Alpha

Have been daily driving this for a while now. Should be a noticeable improvement overall but there may be poor behavior at low speeds when coming to a stop and starting from a stop.

# Upstream
https://github.com/commaai/openpilot/pull/27867

# Detailed Explanation of Change
Calculate jerk from the acceleration plan and use as the lower limit value when sending accel commands to hyundai can vehicles.

Using small min values for the jerk increases the resolution of the acceleration that the car provides. This allows the car to better fit the acceleration to the plan by making smaller adjustments to the acceleration to maintain/hit the target acceleration.

However, with too small of values for either the min or max jerk the car responds to changes in acceleration very sluggishly. Thus when we are requesting rapid changes to acceleration we need larger jerk values.

To achieve a good balance of resolution to responsiveness we can determine what the jerk in the planned acceleration is between the last acc command and the current command and use that as the basis of the values we request from the car. This allows a dynamic resolution that matches the current demands of the plan.
