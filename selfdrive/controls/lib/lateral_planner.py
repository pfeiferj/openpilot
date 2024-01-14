import numpy as np
from openpilot.selfdrive.controls.lib.drive_helpers import CONTROL_N, MIN_SPEED, get_speed_error
from openpilot.selfdrive.controls.lib.desire_helper import DesireHelper
import cereal.messaging as messaging
from cereal import log
# PFEIFER - LD {{
from openpilot.selfdrive.controls.lane_detection import ld
# }} PFEIFER - LD
# PFEIFER - DLP {{
from openpilot.selfdrive.controls.lib.lateral_mpc_lib.lat_mpc import LateralMpc, N as LAT_MPC_N
from openpilot.selfdrive.controls.lib.lane_planner import LanePlanner
from openpilot.common.realtime import DT_MDL
from openpilot.common.numpy_fast import interp
PATH_COST = 1.0
LATERAL_MOTION_COST = 0.11
LATERAL_ACCEL_COST = 0.0
LATERAL_JERK_COST = 0.04
# Extreme steering rate is unpleasant, even
# when it does not cause bad jerk.
# TODO this cost should be lowered when low
# speed lateral control is stable on all cars
STEERING_RATE_COST = 700.0
# }} PFEIFER - DLP

TRAJECTORY_SIZE = 33
CAMERA_OFFSET = 0.04

class LateralPlanner:
  def __init__(self, CP, debug=False):
    self.DH = DesireHelper()
    # PFEIFER - DLP {{
    self.LP = LanePlanner(self.DH)
    self.lat_mpc = LateralMpc()
    self.reset_mpc(np.zeros(4))

    self.plan_yaw = np.zeros((TRAJECTORY_SIZE,))
    self.plan_yaw_rate = np.zeros((TRAJECTORY_SIZE,))
    self.t_idxs = np.arange(TRAJECTORY_SIZE)
    self.y_pts = np.zeros((TRAJECTORY_SIZE,))
    # }} PFEIFER - DLP

    # Vehicle model parameters used to calculate lateral movement of car
    self.factor1 = CP.wheelbase - CP.centerToFront
    self.factor2 = (CP.centerToFront * CP.mass) / (CP.wheelbase * CP.tireStiffnessRear)
    self.last_cloudlog_t = 0
    self.solution_invalid_cnt = 0

    self.path_xyz = np.zeros((TRAJECTORY_SIZE, 3))
    self.velocity_xyz = np.zeros((TRAJECTORY_SIZE, 3))
    self.v_plan = np.zeros((TRAJECTORY_SIZE,))
    self.x_sol = np.zeros((TRAJECTORY_SIZE, 4), dtype=np.float32)
    self.v_ego = MIN_SPEED
    self.l_lane_change_prob = 0.0
    self.r_lane_change_prob = 0.0

    self.debug_mode = debug

  # PFEIFER - DLP {{
  def reset_mpc(self, x0=None):
    if x0 is None:
      x0 = np.zeros(4)
    self.x0 = x0
    self.lat_mpc.reset(x0=self.x0)
  # }} PFEIFER - DLP

  def update(self, sm):
    v_ego_car = sm['carState'].vEgo

    # Parse model predictions
    md = sm['modelV2']
    if len(md.position.x) == TRAJECTORY_SIZE and len(md.velocity.x) == TRAJECTORY_SIZE and len(md.lateralPlannerSolution.x) == TRAJECTORY_SIZE:
      self.path_xyz = np.column_stack([md.position.x, md.position.y, md.position.z])
      self.velocity_xyz = np.column_stack([md.velocity.x, md.velocity.y, md.velocity.z])
      car_speed = np.linalg.norm(self.velocity_xyz, axis=1) - get_speed_error(md, v_ego_car)
      self.v_plan = np.clip(car_speed, MIN_SPEED, np.inf)
      self.v_ego = self.v_plan[0]
      self.x_sol = np.column_stack([md.lateralPlannerSolution.x, md.lateralPlannerSolution.y, md.lateralPlannerSolution.yaw, md.lateralPlannerSolution.yawRate])

    # Lane change logic
    desire_state = md.meta.desireState
    if len(desire_state):
      self.l_lane_change_prob = desire_state[log.LateralPlan.Desire.laneChangeLeft]
      self.r_lane_change_prob = desire_state[log.LateralPlan.Desire.laneChangeRight]
    lane_change_prob = self.l_lane_change_prob + self.r_lane_change_prob
    # PFEIFER - LD {{
    ld.update(md)
    # }} PFEIFER - LD
    self.DH.update(sm['carState'], sm['carControl'].latActive, lane_change_prob)
    # PFEIFER - DLP {{
    self.LP.parse_model(md)
    if self.LP.use_lane_planner(v_ego_car):
      self.path_xyz = self.LP.get_d_path(self.v_ego, self.path_xyz)
      self.lat_mpc.set_weights(PATH_COST, LATERAL_MOTION_COST,
                               LATERAL_ACCEL_COST, LATERAL_JERK_COST,
                               STEERING_RATE_COST)

      y_pts = self.path_xyz[:LAT_MPC_N+1, 1]
      heading_pts = self.plan_yaw[:LAT_MPC_N+1]
      yaw_rate_pts = self.plan_yaw_rate[:LAT_MPC_N+1]
      self.y_pts = y_pts

      assert len(y_pts) == LAT_MPC_N + 1
      assert len(heading_pts) == LAT_MPC_N + 1
      assert len(yaw_rate_pts) == LAT_MPC_N + 1
      lateral_factor = np.clip(self.factor1 - (self.factor2 * self.v_plan**2), 0.0, np.inf)
      p = np.column_stack([self.v_plan, lateral_factor])
      self.lat_mpc.run(self.x0,
                       p,
                       y_pts,
                       heading_pts,
                       yaw_rate_pts)
      # init state for next iteration
      # mpc.u_sol is the desired second derivative of psi given x0 curv state.
      # with x0[3] = measured_yaw_rate, this would be the actual desired yaw rate.
      # instead, interpolate x_sol so that x0[3] is the desired yaw rate for lat_control.
      self.x0[3] = interp(DT_MDL, self.t_idxs[:LAT_MPC_N + 1], self.lat_mpc.x_sol[:, 3])

      #  Check for infeasible MPC solution
      mpc_nans = np.isnan(self.lat_mpc.x_sol[:, 3]).any()
      if mpc_nans or self.lat_mpc.solution_status != 0:
        self.reset_mpc()
        self.x0[3] = sm['controlsState'].curvature * self.v_ego

      if self.lat_mpc.cost > 1e6 or mpc_nans:
        self.solution_invalid_cnt += 1
      else:
        self.solution_invalid_cnt = 0
    # }} PFEIFER - DLP

  def publish(self, sm, pm):
    plan_send = messaging.new_message('lateralPlan')
    plan_send.valid = sm.all_checks(service_list=['carState', 'controlsState', 'modelV2'])

    lateralPlan = plan_send.lateralPlan
    lateralPlan.modelMonoTime = sm.logMonoTime['modelV2']
    lateralPlan.dPathPoints = self.path_xyz[:,1].tolist()
    lateralPlan.psis = self.x_sol[0:CONTROL_N, 2].tolist()

    lateralPlan.curvatures = (self.x_sol[0:CONTROL_N, 3]/self.v_ego).tolist()
    lateralPlan.curvatureRates = [float(0) for _ in range(CONTROL_N-1)] # TODO: unused

    lateralPlan.mpcSolutionValid = bool(1)
    lateralPlan.solverExecutionTime = 0.0
    if self.debug_mode:
      lateralPlan.solverState = log.LateralPlan.SolverState.new_message()
      lateralPlan.solverState.x = self.x_sol.tolist()

    lateralPlan.desire = self.DH.desire
    lateralPlan.useLaneLines = False
    lateralPlan.laneChangeState = self.DH.lane_change_state
    lateralPlan.laneChangeDirection = self.DH.lane_change_direction

    pm.send('lateralPlan', plan_send)
