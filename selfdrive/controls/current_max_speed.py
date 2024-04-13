from openpilot.common.conversions import Conversions as CV
from openpilot.common.params import Params
import json
mem_params = Params("/dev/shm/params")

class CurrentMaxSpeed:
  def __init__(self) -> None:
    self.max_speed = 0

  @property
  def max_speed(self) -> float:
    try:
      return json.loads(mem_params.get("CurrentMaxSpeed"))
    except:
      return 0

  @max_speed.setter
  def max_speed(self, max_speed: float):
    try:
      mem_params.put("CurrentMaxSpeed", json.dumps(float(max_speed)))
    except: pass

  @property
  def max_speed_mph(self) -> float:
    return self.max_speed * CV.MS_TO_MPH

  @max_speed_mph.setter
  def max_speed_mph(self, max_speed: float):
    self.max_speed = max_speed * CV.MPH_TO_MS

  @property
  def max_speed_kph(self) -> float:
    return self.max_speed * CV.MS_TO_KPH

  @max_speed_kph.setter
  def max_speed_kph(self, max_speed: float):
    self.max_speed = max_speed * CV.KPH_TO_MS

cms = CurrentMaxSpeed()
