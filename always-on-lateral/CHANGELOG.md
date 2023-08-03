# Always On Lateral Changelog

## 08/03/23
Panda:
    * Add missing comment block (thanks @nworby for the find!)

## 07/28/23
Openpilot:
    * Disable lateral whenever openpilot is not calibrated

## 07/28/23
Openpilot:
    * Add always\_on\_lateral.py to the release files list (thanks @nworby for the suggestion!)

## 07/07/23
Panda:
    * Remove lateral brake disable check from panda safety when AOL is enabled
      due to it being a temporary override rather than permanent disable.
    * Add an alt experience flag for immediately engaging lateral upon toggling
      cruise main on.
    * Fix for GM\_ASMC always on lateral: lateral\_controls\_allowed was not
      being set to false after the main cruise button was toggled off.

Openpilot:
    * Add a toggle for engaging lateral immediately upon main cruise being
      toggled on.
    * Add warning to test always on lateral in a safe environment upon enabling
      the setting.
    * Add warning to test engaging always on lateral upon cruise main being
      toggled in a safe environment upon enabling the setting.

## 07/01/23
Always On Lateral toggle is disabled when on-road.

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
