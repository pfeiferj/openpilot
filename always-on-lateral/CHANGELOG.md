# Always On Lateral Changelog

## 06/30/23
* Untested support for VW/Audi/Skoda

## 06/16/23
* Rebrand to "Always On Lateral" as feature set isn't identical to "MADS"
* Now requires openpilot to be engaged at least once after main is toggled on
* Fixes for HKG stock long
* Untested support for the following vehicles:
    - Chrysler
    - Ford
    - GM
    - Honda
    - HKG can-fd
    - Mazda
    - Subaru
    - Tesla
    - Toyota

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
* Fixed issue preventing warnings from activating when lateral was on without long control on.
* Resolved merge conflicts with master
