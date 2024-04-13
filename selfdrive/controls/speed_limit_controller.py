from openpilot.common.params import Params
from openpilot.common.conversions import Conversions as CV
from openpilot.selfdrive.controls.gap_adjust_button import gap_adjust_button, GapButtonState
import json
import math

mem_params = Params("/dev/shm/params")
params = Params()

R = 6373000.0 # approximate radius of earth in meters
TO_RADIANS = math.pi / 180
TO_DEGREES = 180 / math.pi
NEXT_SPEED_DIST = 5 # seconds

# points should be in radians
# output is meters
def distance_to_point(ax, ay, bx, by):
  a = math.sin((bx-ax)/2)*math.sin((bx-ax)/2) + math.cos(ax) * math.cos(bx)*math.sin((by-ay)/2)*math.sin((by-ay)/2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

  return R * c  # in meters

class SpeedLimitController:
  nav_speed_limit: float = 0 # m/s
  map_speed_limit: float = 0 # m/s
  next_map_speed_limit: float = 0 # m/s
  next_map_speed_limit_lat: float = 0 # deg
  next_map_speed_limit_lon: float = 0 # deg
  lat: float = 0 # deg
  lon: float = 0 # deg
  car_speed_limit: float = 0 # m/s
  offset: float = 0 # m/s
  nav_enabled: bool = False
  car_enabled: bool = False
  speed_enabled: bool = False
  last_transition_id: int = 0
  current_max_velocity_update_count: int = 0
  current_velocity: float = 0

  def __init__(self) -> None:
    self.load_persistent_enabled()
    self.write_nav_state()
    self.write_map_state()
    self.write_car_state()
    self.write_offset_state()

  def update_current_max_velocity(self, max_v: float, v_ego: float, load_state: bool = True, write_state: bool = True) -> None:
    self.current_velocity = v_ego
    self.current_max_velocity_update_count += 1
    self.current_max_velocity_update_count = self.current_max_velocity_update_count % 100
    if load_state:
      self.load_state()
      if self.current_max_velocity_update_count == 0:
        self.load_persistent_enabled()

    gap_adjust_button.load_state()
    if self.last_transition_id != gap_adjust_button.simple_transition_id:
      self.last_transition_id = gap_adjust_button.simple_transition_id
      if gap_adjust_button.simple_state == GapButtonState.DOUBLE_PRESS:
        if max_v > 0 and max_v < 38 and self.speed_limit > 0:
          self.offset = max_v - self.speed_limit
          if write_state:
            self.write_offset_state()

  @property
  def speed_limit(self) -> float:
    limit: float = 0
    if self.map_enabled and self.next_map_speed_limit != 0:
      d = distance_to_point(self.lat * TO_RADIANS, self.lon * TO_RADIANS, self.next_map_speed_limit_lat * TO_RADIANS, self.next_map_speed_limit_lon * TO_RADIANS)
      max_d = NEXT_SPEED_DIST * self.current_velocity
      if d < max_d:
        return self.next_map_speed_limit

    if self.nav_enabled and self.nav_speed_limit != 0:
      limit = self.nav_speed_limit
    elif self.map_enabled and self.map_speed_limit != 0:
      limit = self.map_speed_limit
    elif self.car_enabled and self.car_speed_limit != 0:
      limit = self.car_speed_limit

    return limit

  @property
  def speed_limit_mph(self) -> float:
    return self.speed_limit * CV.MS_TO_MPH

  @property
  def speed_limit_kph(self) -> float:
    return self.speed_limit * CV.MS_TO_KPH

  @property
  def offset_mph(self) -> float:
    return self.offset * CV.MS_TO_MPH

  @property
  def offset_kph(self) -> float:
    return self.offset * CV.MS_TO_KPH

  def write_nav_state(self):
    mem_params.put("NavSpeedLimit", json.dumps(self.nav_speed_limit))
    mem_params.put_bool("NavSpeedLimitControl", self.nav_enabled)

  def write_map_state(self):
    mem_params.put("MapSpeedLimit", json.dumps(self.map_speed_limit))
    mem_params.put_bool("MapSpeedLimitControl", self.map_enabled)

  def write_car_state(self):
    mem_params.put("CarSpeedLimit", json.dumps(self.car_speed_limit))
    mem_params.put_bool("CarSpeedLimitControl", self.car_enabled)

  def write_offset_state(self):
    mem_params.put("SpeedLimitOffset", json.dumps(self.offset))

  def load_state(self, load_persistent_enabled=False):
    self.nav_enabled = mem_params.get_bool("NavSpeedLimitControl")
    self.car_enabled = mem_params.get_bool("CarSpeedLimitControl")
    self.map_enabled = mem_params.get_bool("MapSpeedLimitControl")
    self.offset = json.loads(mem_params.get("SpeedLimitOffset"))
    self.nav_speed_limit = json.loads(mem_params.get("NavSpeedLimit"))
    self.map_speed_limit = json.loads(mem_params.get("MapSpeedLimit"))
    try:
      next_map_speed_limit = json.loads(mem_params.get("NextMapSpeedLimit"))
      self.next_map_speed_limit = next_map_speed_limit["speedlimit"]
      self.next_map_speed_limit_lat = next_map_speed_limit["latitude"]
      self.next_map_speed_limit_lon = next_map_speed_limit["longitude"]
    except: pass
    try:
      position = json.loads(mem_params.get("LastGPSPosition"))
      self.lat = position["latitude"]
      self.lon = position["longitude"]
    except: pass
    self.car_speed_limit = json.loads(mem_params.get("CarSpeedLimit"))

    if load_persistent_enabled:
      self.load_persistent_enabled()

  def load_persistent_enabled(self):
    self.nav_enabled = params.get_bool("NavSpeedLimitControl")
    self.car_enabled = params.get_bool("CarSpeedLimitControl")
    self.map_enabled = params.get_bool("MapSpeedLimitControl")
    mem_params.put_bool("NavSpeedLimitControl", self.nav_enabled)
    mem_params.put_bool("MapSpeedLimitControl", self.map_enabled)
    mem_params.put_bool("CarSpeedLimitControl", self.car_enabled)


  def write_persistent_enabled(self):
    params.put_bool("NavSpeedLimitControl", self.nav_enabled)
    params.put_bool("CarSpeedLimitControl", self.car_enabled)
    params.put_bool("MapSpeedLimitControl", self.map_enabled)


slc = SpeedLimitController()
