# Ford Steering Hack
Hack as in not a proper way to fix things but it works well enough. Tries to
solve an issue where after overriding for a sharp curve the wheel is pulled as
if you are still in the curve. This patch ignores angle rate limits while the
driver is overriding the steering, this allows the planned angles to keep up
with the current state of the wheel. However, this results in panda blocking a
single message each time the angle limits are exceeded. Typically panda is
blocking while the user is overriding so is not even noticeable, however it
could block up to one message after the user stops overriding.

## Branch
[pfeifer-ford-steering-hack](https://github.com/pfeiferj/openpilot/tree/pfeifer-ford-steering-hack)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-ford-steering-hack)

## Status
Hacky

## Comment Blocks Text
PFEIFER - FSH
