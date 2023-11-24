from openpilot.common.params import Params
from openpilot.common.conversions import Conversions as CV
import json
import math
from openpilot.common.numpy_fast import interp
from time import time

mem_params = Params("/dev/shm/params")
params = Params()

R = 6373000.0 # approximate radius of earth in meters
TO_RADIANS = math.pi / 180
TO_DEGREES = 180 / math.pi
TARGET_JERK = -1.0 # m/s^3 should match up with the long planner
MIN_ACCEL = -3.5 # m/s^2 should match up with the long planner

# points should be in radians
# output is meters
def distance_to_point(ax, ay, bx, by):
  a = math.sin((bx-ax)/2)*math.sin((bx-ax)/2) + math.cos(ax) * math.cos(bx)*math.sin((by-ay)/2)*math.sin((by-ay)/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

  return R * c  # in meters

class MapTurnSpeedController:
  def __init__(self):
    self.enabled = params.get_bool("MTSCEnabled")
    self.last_params_update = time()

  def update_params(self):
    t = time()
    if t > self.last_params_update + 5.0:
      self.enabled = params.get_bool("MTSCEnabled")
      self.last_params_update = t

  def target_speed(self, v_ego, a_ego) -> float:
    self.update_params()

    if not self.enabled:
      return 0.0

    lat = 0.0
    lon = 0.0
    try:
      position = json.loads(mem_params.get("LastGPSPosition"))
      lat = position["latitude"]
      lon = position["longitude"]
    except: return 0.0

    try:
      target_velocities = json.loads(mem_params.get("MapTargetVelocities"))
    except: return 0.0

    min_dist = 1000
    min_idx = 0
    distances = []

    # find our location in the path
    for i in range(len(target_velocities)):
      target_velocity = target_velocities[i]
      tlat = target_velocity["latitude"]
      tlon = target_velocity["longitude"]
      d = distance_to_point(lat * TO_RADIANS, lon * TO_RADIANS, tlat * TO_RADIANS, tlon * TO_RADIANS)
      distances.append(d)
      if d < min_dist:
        min_dist = d
        min_idx = i

    # only look at values from our current position forward
    forward_points = target_velocities[min_idx:]
    forward_distances = distances[min_idx:]

    # find velocities that we are within the distance we need to adjust for
    valid_velocities = []
    for i in range(len(forward_points)):
      target_velocity = forward_points[i]
      tlat = target_velocity["latitude"]
      tlon = target_velocity["longitude"]
      tv = target_velocity["velocity"]
      if tv > v_ego:
        continue

      d = forward_distances[i]
      min_accel_t = max(0.1, (MIN_ACCEL - a_ego) / TARGET_JERK) # seconds to reach min accel
      min_jerk_v = 0.5 * TARGET_JERK * min_accel_t ** 2 + a_ego + v_ego # the minimum v we can reach before hitting the min accel limit
      t = 0.0
      if tv > min_jerk_v:
        # calculate time needed based on jerk
        a = 0.5 * TARGET_JERK
        b = a_ego
        c = v_ego - tv
        t_a = (-1 * b - math.sqrt((b ** 2) - 4 * a * c)) / (2 * a)
        t_b = (-1 * b + math.sqrt((b ** 2) - 4 * a * c)) / (2 * a)
        if t_a > 0:
          t = t_a
        else:
          t = t_b
      else:
        # calculate time needed based on hitting the min accel
        t = min_accel_t + ((min_jerk_v - tv) / (-1 * MIN_ACCEL))

      # Adjust slightly early so we get to the speed before hitting the curve
      t += 3.0
      max_d = t * v_ego
      if d < max_d:
        valid_velocities.append(float(tv))

    # Find the smallest velocity we need to adjust for
    min_v = 100.0
    for tv in valid_velocities:
      if tv < min_v:
        min_v = tv


    return min_v

mtsc = MapTurnSpeedController()
