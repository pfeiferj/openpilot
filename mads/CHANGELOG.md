# MADS Changelog

## 06/11/23
* Improved panda safety code that ensures stock behavior when the alt experience
  is not set.
* Raised the minimum lockout speed to try to reduce wheel pull when coming to a
  stop
* Uses /dev/shm for lateral\_allowed param to prevent lag. We still write
  lateral\_allowed to the regular params location for the ui but we use a
  nonblocking put as we now do not need it to be perfectly in sync when reading.

## 06/03/23
* Improved panda safety code that enforces the alt experience flag to be sent
  from openpilot.
* Added a disable at stopped speeds to prevent wheel twitching when stopped.
* Resolved merge conflicts with master
