# PFEIFER - GAB

# Acknowledgements:
# HKG button state was pulled from sunnypilot. https://github.com/sunnyhaibin/sunnypilot
# GM button state was pulled from OPGM. https://github.com/opgm/openpilot
# Toyota button state was pulled from Frogpilot who pulled it from krkeegan. https://github.com/FrogAi/FrogPilot | https://github.com/krkeegan/openpilot

from openpilot.selfdrive.controls.button_manager import Button, ButtonState

# export button state so only one import is necessary
GapButtonState = ButtonState

gap_adjust_button = Button("GapAdjustButton")
