from openpilot.common.conversions import Conversions as CV
from openpilot.common.realtime import Ratekeeper
#import json
import cereal.messaging as messaging
from openpilot.common.params import Params
import numpy as np
mem_params = Params("/dev/shm/params")

class SpeedZoneD:
  def __init__(self, sm) -> None:
    self.sm = sm
    self.current_zone_speed = 0
    self.zones = [{
      'speed': 20.2,
      'bounds': [39.12595276194359, 39.12849955662224, -83.1195750553161, -83.1160989124328]
    }, {
      'speed': 22.5,
      'bounds': [39.112813862314184, 39.115011512201974, -83.11453342437746, -83.10989856719972]
    }, {
      'speed': 6.7,
      'bounds': [39.14160263623521, 39.14381602982941, -83.1463122367859, -83.14226746559144]
    }, {
      'speed': 6.7,
      'bounds': [39.150144568129676, 39.151575619311245, -83.15425140783192, -83.14918739721182]
    }]
    #f = open('/data/media/0/speed_zones.json')
    #data = json.load(f)
    #f.close()

  def update(self) -> None:
    self.sm.update()
    location = self.sm['liveLocationKalman']
    if location.positionGeodetic.valid:
      self.location_rad = np.radians(np.array([location.positionGeodetic.value[0], location.positionGeodetic.value[1]]))
      self.location_deg = (location.positionGeodetic.value[0], location.positionGeodetic.value[1])
      found = False
      for zone in self.zones:
        if self.location_deg[0] > zone['bounds'][0] and self.location_deg[1] < zone['bounds'][1] and self.location_deg[1] < zone['bounds'][2] and self.location_deg[0] > zone['bounds'][0]:
          mem_params.put('SpeedZonesLimit', str(zone['speed']))
          found = True
      if not found:
        mem_params.put('SpeedZonesLimit', str(0))


def speed_zoned_thread(sm=None, pm=None):
  # *** setup messaging
  if sm is None:
    sm = messaging.SubMaster(['liveLocationKalman'])

  speed_zoned = SpeedZoneD(sm)

  rk = Ratekeeper(.2, print_delay_threshold=None)  # Keeps rate at 5 hz
  while True:
    speed_zoned.update()
    rk.keep_time()


def main(sm=None, pm=None):
  speed_zoned_thread(sm, pm)


if __name__ == "__main__":
  main()
