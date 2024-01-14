# PFEIFER - DBC

import numpy as np
from openpilot.selfdrive.modeld.constants import index_function
import json
from openpilot.selfdrive.modeld.constants import ModelConstants
from openpilot.common.params import Params
mem_params = Params("/dev/shm/params")
params = Params()

CONTROL_N = 17
N = 12
MAX_T = 10.0
T_IDXS_LST = [index_function(idx, max_val=MAX_T, max_idx=N) for idx in range(N+1)]

T_IDXS_MPC = np.array(T_IDXS_LST)

class DistanceBasedCurvature:
  def __init__(self):
    self.enabled = params.get_bool("DistanceBasedCurvature")

  @property
  def distances(self):
    distances = mem_params.get("Distances")
    if distances is not None:
      distances = json.loads(distances.decode())
      distances = np.interp(ModelConstants.T_IDXS, T_IDXS_MPC, distances)
      distances = distances[:CONTROL_N].tolist()
    else:
      distances = []

    if len(distances) != CONTROL_N:
      distances = [0.0] * CONTROL_N

    return distances


  @distances.setter
  def distances(self, distances):
    mem_params.put("Distances", json.dumps(distances.tolist()))


  def average_curvature_desired(self, psi, v_ego, delay):
    distances = self.distances
    distance = np.interp(delay, ModelConstants.T_IDXS[:CONTROL_N], distances)
    distance = max(0.0001, distance)
    average_curvature_desired = psi / distance if self.enabled else psi / (v_ego * delay)
    if isinstance(average_curvature_desired, float):
      return average_curvature_desired
    return average_curvature_desired.item()

dbc = DistanceBasedCurvature()
