# Mission 1 → mission 11: first field trial

This replaces the earlier mission 6 plan. Start at the exact position and orientation where mission 1 finishes. The supplied route is entered in `mission11.py`:

1. Reverse 150 mm.
2. Turn left 90°.
3. Forward 600 mm.
4. Turn right 90°.
5. Forward 250 mm.
6. Turn right 45°.
7. Accelerate straight forward to bump.
8. Brake, pause 150 ms, reverse 60 mm.

## Settings and testing

`SETUP_CONFIRMED = True` and `ENABLE_BUMP = True`: this trial runs the route and bump immediately. Set `ENABLE_BUMP = False` for a route-only trial that stops after the last turn. The route has not been tested on the robot.

Travel is 150 mm/s; turns are 60°/s. Straight acceleration is 400 mm/s² and turn acceleration is 250°/s². Initial bump target speed is 200 mm/s, using the same straight acceleration. Bumping stops at the first of 650 ms, 100 mm estimated wheel travel, or detected stall. The time includes acceleration and approach, so a large gap may leave it short. A stop reason is not proof of scoring. Check that the root cover actually opens fully.

Tune `BUMP_SPEED` in 25–50 mm/s steps with a consistent gap and acceleration. Use the lowest speed that succeeds reliably. Adjust limits only after checking the actual final gap and contact point. The retreat is 60 mm; check its clearance. There is no return-home route.

## Mission 1 handoff

Finish all pending drive and attachment movements before starting mission 11. Forklift height after mission 1 has not been specified; this script leaves attachment motors unchanged. Ensure the forklift clears the route. The long black arm is not used. The earlier leaf-cutter starting position and lowered-forklift assumption no longer apply.

Standalone setup retains the repository defaults: left motor A counterclockwise, right motor B clockwise, 43 mm wheels, 114 mm axle track. Verify these match the working mission 1 program. Combined runs reuse its DriveBase without resetting its gyro.

## Pybricks integration

For standalone testing, import or paste `mission11.py` into Pybricks. Position the robot at mission 1's ending pose. Starting it runs the route and bump; it does not execute mission 1 first.

For the combined run, import `mission11.py` alongside the existing team program:

```python
from mission11 import mission11_after_mission1

def combined_run():
    mission1()  # Replace with your actual working mission 1 function.
    mission11_after_mission1(drive_base)
```

The entry point is now `mission11_after_mission1`; update any old `mission11_after_mission6` imports/calls. The working mission 1 code has not been provided, so this is an integration example, not a replacement for that code.

Alternatively paste the portion ABOVE the standalone-practice section into the team program before its run functions and final `main()` call. Call `mission11_after_mission1(drive_base)` immediately after mission 1. Do not reinitialize motors or call another `start_run()` between missions. The function brakes on exit and restores incoming drive settings.

## Existing launcher note

The inspected upstream `main.py` has `(Color,GREEN, 4, left_run4, right_run4)`; change it to `(Color.GREEN, 4, left_run4, right_run4)`. Add `Color.GREEN` to `sensor.detectable_colors(...)` if using that fourth run. This branch does not change the launcher or its example missions.

## Validation

Local software simulation covers route order and signs, enabled bump, retreat, route-only mode, obstruction/timeout aborts, braking, and settings restoration. Physical route accuracy and scoring still require field trials.

References: [team framework](https://github.com/kenaucrebot/2026/blob/main/main.py), [Pybricks DriveBase API](https://docs.pybricks.com/en/latest/robotics.html).
