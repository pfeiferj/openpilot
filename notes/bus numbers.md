# Bus Definitions
Big thanks to @sunnyhaibin and @AlexandreSato for explaining these.

## Can buses:
* Bus 0-3 are stock messages
  - 0 - main bus (car side)
  - 1 - radar bus
  - 2 - camera bus
  - 3 - ELM327 for fingerprint purposes and only is multiplexed from bus 1 on init
* Bus 128-131 are messages sent by openpilot
  - add 128 to the stock bus to match the openpilot bus
* Bus 192-195 are messages blocked by panda
  - add 192 to the stock bus to match the openpilot bus

## Can-fd buses:
* Bus 4-6 are stock messages
* Bus 132-134 are messages sent by openpilot
  - add 128 to the stock bus to match the openpilot bus
* Bus 196-198 are messages blocked by panda
  - add 192 to the stock bus to match the openpilot bus
