# PFEIFER - GAC
# Acknowledgements:
# HKG dashboard display pulled from sunnypilot. https://github.com/sunnyhaibin/sunnypilot
# GM dashboard display pulled from OPGM. https://github.com/opgm/openpilot

from openpilot.common.params import Params
from enum import IntEnum
from openpilot.selfdrive.controls.gap_adjust_button import gap_adjust_button, GapButtonState

params = Params()

class GapAdjustState(IntEnum):
  AGGRESSIVE = 0
  STANDARD = 1
  RELAXED = 2

class GapAdjust:
  state: GapAdjustState = GapAdjustState.STANDARD
  button_transition_id = 0
  disable_default_update = False

  def __init__(self) -> None:
    self.load_state()

  def load_state(self) -> None:
    try:
      self.state = GapAdjustState(int(params.get('LongitudinalPersonality')))
    except:
      self.state = GapAdjustState.STANDARD

  def write_state(self) -> None:
    params.put_nonblocking('LongitudinalPersonality', str(int(self.state)))

  def update(self, load_state=True, write_state=True, load_button_state=True) -> None:
    if self.disable_default_update:
      return

    if load_button_state:
      gap_adjust_button.load_state()

    transition_id = gap_adjust_button.simple_transition_id;

    if self.button_transition_id != transition_id:
      self.button_transition_id = transition_id
      if gap_adjust_button.simple_state == GapButtonState.SINGLE_PRESS:
        if load_state:
          self.load_state()

        self.state = GapAdjustState((int(self.state) + 1) % 3)

        if write_state:
          self.write_state()

  def transition_car_state(self, load_button_state=True):
    transition_id = gap_adjust_button.simple_transition_id;

    if self.button_transition_id != transition_id:
      self.button_transition_id = transition_id
      if gap_adjust_button.simple_state == GapButtonState.SINGLE_PRESS:
        return True

    return False


  def update_from_car_state(self, state: GapAdjustState, write_state=True) -> None:
    self.disable_default_update = True

    old_state = self.state
    self.state = GapAdjustState(state % 3)

    if write_state and old_state != self.state:
      self.write_state()

gap_adjust = GapAdjust()
