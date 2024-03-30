# PFEIFER - VTSC

# Acknowledgements:
# Past versions of this code were based on the move-fast teams vtsc
# implementation. (https://github.com/move-fast/openpilot) Huge thanks to them
# for their initial implementation. I also used sunnypilot as a reference.
# (https://github.com/sunnyhaibin/sunnypilot) Big thanks for sunny's amazing work

import numpy as np
from time import time
from openpilot.common.params import Params
params = Params()

TARGET_LAT_A = 1.9 # m/s^2
MIN_TARGET_V = 5 # m/s

class VisionTurnController():
  def __init__(self):
    self.op_enabled = False
    self.gas_pressed = False
    self.last_params_update = 0
    self.enabled = params.get_bool("TurnVisionControl")
    self.v_target = MIN_TARGET_V


  @property
  def active(self):
    return self.op_enabled and not self.gas_pressed and self.enabled

  def update_params(self):
    t = time()
    if t > self.last_params_update + 5.0:
      self.enabled = params.get_bool("TurnVisionControl")
      self.last_params_update = t

  def update(self, op_enabled, v_ego, sm):
    self.update_params()
    self.op_enabled = op_enabled
    self.gas_pressed = sm['carState'].gasPressed

    rate_plan = np.array(np.abs(sm['modelV2'].orientationRate.z))
    vel_plan = np.array(sm['modelV2'].velocity.x)

    # get the maximum lat accel from the model
    predicted_lat_accels = rate_plan * vel_plan
    self.max_pred_lat_acc = np.amax(predicted_lat_accels)

    # get the maximum curve based on the current velocity
    v_ego = max(v_ego, 0.1) # ensure a value greater than 0 for calculations
    max_curve = self.max_pred_lat_acc / (v_ego**2)

    # Get the target velocity for the maximum curve
    self.v_target = (TARGET_LAT_A / max_curve) ** 0.5
    self.v_target = max(self.v_target, MIN_TARGET_V)

vtsc = VisionTurnController()
