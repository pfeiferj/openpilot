# VTSC Changelog

## 10/14/2023
Rewrite to be significantly simpler
* No longer tries to detect distance to curve
* No longer tries to calculate an acceleration curve, only sets max velocity
* Now uses curvature rates from model rather than calculating curvature from path

## 06/11/2023
* Corrected improper calculations.
* Now tracks the mathematically highest point of curvature in the polynomial.
* Temporarily removed calculation of current lateral accel due to upstream PR
  being rejected.
* Uses jerk limits to smooth out requested acceleration instead of a filter.
