# VTSC Changelog
## 06/11/2023
* Corrected improper calculations.
* Now tracks the mathematically highest point of curvature in the polynomial.
* Temporarily removed calculation of current lateral accel due to upstream PR
  being rejected.
* Uses jerk limits to smooth out requested acceleration instead of a filter.
