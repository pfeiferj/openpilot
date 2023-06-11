# Button Manager
A utility class for tracking different types of button presses. Buttons are also
given a custom name which makes it easier to support multiple car types as you
can use a consistent button name across all car types.

This doesn't add any features to openpilot itself and is intended to be used
when building other patches.

## Branch
[pfeifer-button-manager](https://github.com/pfeiferj/openpilot/tree/pfeifer-button-manager)
\-
[diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-button-manager)

## Status
Alpha

Known working but may need tweaks for supporting cars with different ways of
handling buttons.

## Comment Blocks Text
PFEIFER - BM

## API Usage

### Creating a button
Create a button by adding a param to common/params.cc, the param name will be
the button name you bass into the Button class when creating an instance of a
button.


common/params.cc:
```c++
// Note that we are only using the PERSISTENT flag because we need to pass a
// flag in. The button state will not actually be persistent across reboots
// because the Button class writes the param to /dev/shm/params which is a
// volatile directory stored in memory.
{"MyButtonName", PERSISTENT},
```
Creating in python:
```python
from selfdrive.controls.button_mannager import Button, ButtonState
my_button = Button("MyButtonName")
```

### Updating the button state
To update the state of the button you simply pass in to the update function
whether the button is currently pressed or not.

```python
button_is_pressed: bool = # your car specific code
my_button.update(button_is_pressed)
```

### Using the button state
There are two primary values for determining the state of the button. The state
property and the transition\_id property. The state property contains the last
type of button press, i.e. a single or double press, that has happened. The
transition\_id counts the number of times the button has transitioned. By
storing the transition id whenever you do an action based on a state you can
then check if you are seeing a new state by if the transition id does not match
the one you have stored.

```python
# button defined elsewhere
from my_button import my_button
from selfdrive.controls.button_manager import ButtonState

prev_my_button_transition_id = 0
def update():
    # check if the button has transitioned state
    if my_button.transition_id != prev_my_button_transition_id:
        prev_my_button_transition_id = my_button.transition_id

        # we are guaranteed this is a new state so check if it's a double press
        if my_button.state == ButtonState.DOUBLE_PRESS:
            do_something()

```

### State vs Simple State
One thing to note about the state value is that it could be in a "transitionary"
state, or in other words a non-final state. If you are only checking against
final states this may not matter to you but there are some transitionary states
that could be considered "equivalent" to a different final state. For example
LONG\_PRESS\_WAITING\_RELEASE will only ever move to LONG\_PRESS and could
functionally be considered the same if you don't care about waiting for the user
to release the button. To make the logic for handling this simpler there is a
simple\_state and simple\_transition\_id property that can be used in the same
way as state and transition\_id.

```python
# button defined elsewhere
from my_button import my_button
from selfdrive.controls.button_manager import ButtonState

prev_my_button_transition_id = 0
def update():
    # check if the button has transitioned state
    if my_button.simple_transition_id != prev_my_button_transition_id:
        prev_my_button_transition_id = my_button.simple_transition_id

        # we are guaranteed this is a new state so check if it's a double press
        if my_button.simple_state == ButtonState.DOUBLE_PRESS:
            do_something()

```

### Complete Example
[experimental-mode-toggle](https://github.com/pfeiferj/openpilot/tree/pfeifer-openpilot-patches/experimental-mode-toggle)
contains a simple example of the button manager being used.


[This diff](https://github.com/commaai/openpilot/compare/master...pfeiferj:openpilot:pfeifer-experimental-mode-toggle)
contains the relevant code in the following files:
* common/params.cc
* selfdrive/car/hyundai/interface.py
* selfdrive/controls/experimental\_mode\_toggle.py
* selfdrive/controls/gap\_adjust\_button.py
