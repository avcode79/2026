# Reusable forklift module

Port C moved the forklift in the button test. The upward sign and complete travel are not yet confirmed: the response to the direction test did not specify whether the first movement went up or down.

`forklift.py` defines `Forklift`. Importing it does not create motors or move anything. It uses timed monitoring of position moves and holds at the completed position. No current mission script has been changed to use it yet.

## Calibrate first

- The test used CLOCKWISE as positive. If the FIRST movement raised the forklift, use `UP_DIRECTION = 1`. If it lowered it, use `-1`.
- Measure motor-shaft rotation from the repeatable lowered position to your desired raised position. Use the absolute measured difference as `RAISED_DEGREES`. The timed identification test did not establish full travel. These are motor degrees, not millimeters; include the effect of the actual gears by measuring the motor rotation.
- Leave clearance before the mechanical end stops. Do not guess full travel from the small jog.
- At 100 degrees/second, a 5000 ms timeout may be too short for long travel. Choose a timeout above the measured normal duration, with allowance for acceleration.

## Future run integration

Create/import `forklift.py` in the same Pybricks project as the run. This example deliberately requires calibration values to be filled in:

```python
from forklift import Forklift

UP_DIRECTION = None    # Replace with +1 or -1 after checking the first jog.
RAISED_DEGREES = None  # Replace with measured motor-shaft travel.

lift = Forklift(UP_DIRECTION, RAISED_DEGREES)
# Before starting: place the forklift at the agreed LOWERED position.
lift.zero_at_bottom()  # Defines zero only; does not move or find the bottom.

# Insert these calls at the desired places in a future run:
lift.raise_forklift()
# ...drive, deliver, or perform another task...
lift.lower_forklift()
```

If the run already creates `left_attachment = Motor(Port.C, Direction.CLOCKWISE)`, reuse it rather than initializing Port C twice:

```python
lift = Forklift(UP_DIRECTION, RAISED_DEGREES, motor=left_attachment)
```

The supplied motor must use the same direction/gearing convention used for calibration. Initialize and zero once before the combined run, not between missions. Do not zero while the lift is raised. Do not have another part of the program command the same motor at the same time.

`raise_forklift()` and `lower_forklift()` wait for completion. Repeating either call targets the same absolute position; it does not add another full stroke. `move_to(value)` supports intermediate positions between 0 and RAISED_DEGREES. For example, `move_to(RAISED_DEGREES / 2)` targets half the calibrated motor travel.

After a stall or timeout, the function brakes, invalidates its reference, and raises an error so the run stops. Check the mechanism and establish the lowered reference again before retrying. Passive braking does not guarantee a loaded lift stays up. Successful movement uses active holding while the program is running; ending/stopping the program can release it.

This is not an automatic homing module: a suitable bottom hard stop has not been confirmed. Existing mission cleanup functions that call `left_attachment.stop()` release active holding; account for that when integrating.

Software checks cover both direction signs, absolute raise/lower targets, calibration guards, travel limits, repeated raises, and stall/timeout cleanup. The module has not been tested on the physical robot.

Reference: [Pybricks motor API](https://docs.pybricks.com/en/latest/pupdevices/motor.html).
