# PFEIFER - VTSC

import numpy as np
from time import time
from openpilot.common.params import Params
params = Params()

class LongHelper():
  def __init__(self):
    self.accels = np.array([])
    self.speeds = np.array([])
    self.target_accel = 0
    self.target_speed = 0
    self.precharge = False

  def update(self, accels, speeds):
    self.accels = np.array(accels)
    self.speeds = np.array(speeds)
    if len(self.accels) == 0 or len(self.speeds) == 0:
      self.target_accel = 0
      self.target_speed = 0
      self.precharge = False
      return

    min_speed = np.min(self.speeds)
    max_speed = np.max(self.speeds)
    current_speed = self.speeds[0] if len(self.speeds) > 0 else 0

    min_accel = np.min(self.accels)
    max_accel = np.max(self.accels)
    current_accel = self.accels[0] if len(self.accels) > 0 else 0

    if np.abs(current_speed - min_speed) > np.abs(current_speed - max_speed):
      self.target_speed = min_speed
    else:
      self.target_speed = max_speed

    if np.abs(current_accel - min_accel) >= np.abs(current_accel - max_accel):
      self.target_accel = min_accel
    else:
      self.target_accel = max_accel

    if current_accel - self.target_accel > 0.1 and self.target_accel < 0:
      self.precharge = True
    else:
      self.precharge = False

    self.target_accel = np.clip(self.target_accel, -5, 5)




lh = LongHelper()
