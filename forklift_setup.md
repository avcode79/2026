# Calibrated forklift: Port C

Team-measured settings are saved in `forklift.py`:

- `UP_DIRECTION = 1`: clockwise-positive motor rotation raises the lift.
- `RAISED_DEGREES = 639`: motor-shaft travel from the recorded bottom to the desired top, not millimeters.
- Default speed: 100 motor degrees/second.
- Default timeout: 10 seconds. The previous 5-second limit was too short for a full 639-degree move at 100 degrees/second; nominal travel alone takes 6.39 seconds, before acceleration and settling.

## Use in a future run

Import `forklift.py` into the same Pybricks project as the run. Place the forklift at the SAME physical bottom position used during calibration before starting.

```python
from forklift import Forklift

lift = Forklift()  # Uses calibrated Port C defaults.
lift.zero_at_bottom()  # Records zero; does NOT move or find the bottom.

lift.set_height(50)    # Halfway: 319.5 motor degrees above bottom.
# Perform a task here.
lift.set_height(0)     # Return to bottom.
```

`set_height(100)` targets the calibrated top. Values must be from 0 to 100. `raise_forklift()` and `lower_forklift()` remain available for full up/down. All movements wait for completion and actively hold afterward. Repeated calls target the same position rather than adding travel. Percentages represent a fraction of calibrated motor travel; actual vertical height depends on the linkage.

If a run already creates `left_attachment = Motor(Port.C, Direction.CLOCKWISE)`, reuse it:

```python
lift = Forklift(motor=left_attachment)
```

Do not create two motor objects for C or command it from two parts of the run simultaneously. The existing motor must have the same direction and gearing convention used for calibration. Initialize and zero once at the bottom before a combined run, not between missions. Importing the module alone does not create hardware or move anything.

## Stopping and reference position

On a stall or timeout, the module passively brakes, invalidates its reference, and raises an error. Check the mechanism and reestablish the physical bottom before zeroing again. A passive brake may not hold a loaded lift against gravity. Successful moves use active holding while the program runs; ending/stopping the program can release it. Existing cleanup functions that call `left_attachment.stop()` also release holding.

There is no automatic bottom detection or hard-stop homing. If the lift was moved or the mechanism changed, reestablish the bottom reference or recalibrate as appropriate.

The mission 1 and combined mission scripts have not been changed to operate the forklift yet. This module is ready for future integration. Local software checks cover calibrated defaults, percentages, direction signs, repeated targets, range guards, timeout/stall handling, and cleanup. The measured endpoints come from the user's calibration; full automated cycles still need field testing.

Reference: [Pybricks motor API](https://docs.pybricks.com/en/latest/pupdevices/motor.html).
