# Lateral MPC Costs Tuning
_This was not written by me (Jacob Pfeifer). I found it as a repost on discord
so am not sure who the original author was._

* PATH\_COST (1.0):
    - This value represents the weight given to the path tracking error, i.e.,
      the deviation of the vehicle from the desired path. Increasing this value
      will prioritize staying close to the desired path, while decreasing it may
      result in larger deviations from the path.

* LATERAL\_MOTION\_COST (0.11):
    - This value is the weight given to the lateral motion of the vehicle,
      specifically the heading error. Increasing this value will prioritize
      minimizing the heading error and aligning the vehicle with the desired
      path. Decreasing it may result in larger heading errors.

* LATERAL\_ACCEL\_COST (0.0):
    - This value is the weight given to the lateral acceleration of the vehicle.
      Increasing this value will prioritize minimizing the lateral acceleration,
      resulting in smoother lateral movements. Decreasing it will have the
      opposite effect, potentially causing more abrupt lateral movements.

* LATERAL\_JERK\_COST (0.04):
    - This value is the weight given to the lateral jerk, i.e., the rate of
      change of lateral acceleration. Increasing this value will prioritize
      reducing lateral jerk, leading to smoother changes in lateral
      acceleration. Decreasing it may result in more abrupt changes in lateral
      acceleration.

* STEERING\_RATE\_COST (700.0):
    - This value represents the weight given to the rate of change of the
      steering angle. Increasing this value will prioritize minimizing the rate
      of steering angle changes, resulting in smoother steering movements.
      Decreasing it may lead to more abrupt steering movements.

These weights are used in the set\_weights method of the LateralMpc class to
define the cost function for the MPC optimization problem. By tuning these
values, you can adjust the priorities and overall behavior of the lateral
controller to achieve the desired performance.
