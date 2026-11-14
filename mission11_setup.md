# Armaan's BIOGLOW: mission 6 to mission 11

## Status

The movement and bounded bump routine is implemented in `mission11.py`. The physical route is NOT calibrated or ready for an unattended mission run. Unknown route values are deliberately empty; the program reports what is missing before starting motors. No robot testing has been performed.

Confirmed handoff from mission 6: robot faces the leaf cutter, lever pushed in, forklift fully lowered, long black arm removed. Mission 6 must finish pending motor actions before calling mission 11. Do not reset or reinitialize the existing drive base between missions.

## Fill in the route

Measure from that exact handoff position. Start with a negative straight move to withdraw the forklift completely from the leaf cutter before turning. Check that withdrawing does not pull the lever back out. Plan the remaining straight segments and turns around the models, ending square to the back of mission 11. Allow clearance for the entire robot and lowered forklift as they sweep through turns.

Use entries like `("straight", distance_in_mm)` and `("turn", angle_in_degrees)` in `ROUTE`. Positive straight goes forward, negative reverses; positive turn is right, negative is left. These are relative movements, not compass headings. Measure driving distances at the midpoint between the wheels; measure the final contact gap from the actual bumper face. No example numbers constitute a field route.

Verify the repository defaults (left motor A counterclockwise, right motor B clockwise, 43 mm wheel diameter, 114 mm axle track) against your robot. The photos alone do not establish those measurements. Then set `SETUP_CONFIRMED = True`.

Run with `ENABLE_BUMP = False` first. It stops at the approach position. Adjust the route until this position is repeatable. The lowered forklift needs clearance throughout; no attachment motor is operated by this script.

## Contact strategy

With the long black arm removed, inspect what actually touches the model first. Prefer a short, wide bumper braced to the chassis, at the model's intended contact height, so the impact does not load the lift rack and gears. A rear bumper is another option if the front fork cannot make suitable contact; set `BUMP_DIRECTION = -1` and change the route so the rear faces the target. This is a proposed mechanical approach, not a verified solution for this model.

M11 scores when the root cover is down touching the mat. A bump into the box only works if it actually releases that cover. Test the contact point gently by hand before increasing speed. The program cannot sense whether the mission scored.

Once alignment is repeatable, set `ENABLE_BUMP = True`. Initial test settings are 200 mm/s, at most 650 ms and 100 mm of encoder travel. These are starting test limits, not measured requirements or a guarantee of sufficient force. Increase speed in small steps only after checking contact geometry; stop increasing once release is reliable. The pulse stops on stall, time limit, or travel limit, then retreats 60 mm. Adjust retreat clearance on the field. Wheel slip makes encoder travel unreliable, which is why there is also a time cap. Do not infer scoring from a stall or the printed completion message.

## Use in Pybricks

For standalone practice, create a new Python program in Pybricks Code and paste `mission11.py`, or use its file import option. Place the robot at the agreed M06 ending pose before running. This practice program operates only the drive motors; set and secure the forklift appropriately before starting.

For the combined run, import `mission11.py` alongside the team's program and add:

```python
from mission11 import mission11_after_mission6

def combined_run():
    mission6()  # Replace with the programmer's actual M06 function name.
    mission11_after_mission6(drive_base)
```

Alternatively, paste everything ABOVE the standalone-practice section into the team's file, before its run functions and final `main()` call. Then call `mission11_after_mission6(drive_base)` immediately after M06 completes. Use one run-selector entry for the combined run. Do not launch M11 through a second `start_run()` call, which resets heading. Do not import the repository's `main.py` as a helper: it starts its selection loop on import.

The script restores incoming drive settings and brakes when it exits. It finishes near M11; it does not provide a return-to-home route.

## Existing launcher correction

In the inspected GitHub `main.py`, `(Color,GREEN, 4, left_run4, right_run4)` uses an undefined name. Change it to `(Color.GREEN, 4, left_run4, right_run4)`. Add `Color.GREEN` to `sensor.detectable_colors(...)` if using this fourth run. Existing run bodies are examples, not verified missions.

## Verification and remaining measurements

Local simulated checks passed for configuration refusal, route-only mode, the bump time limit, retreat, route obstruction/timeout aborts, braking, and restoring drive settings. These checks do not establish physical compatibility, route accuracy, impact force, or scoring. Test the combined M06/M11 run repeatedly and record results.

Still needed: reverse clearance from M06, each intervening distance and turn, final bumper-to-model gap and contact height, and confirmation of the actual wheel dimensions/ports. A full-field overhead photo with M06's ending position and the intended M11 contact side marked would help plan the path, but measurements and on-field tuning remain necessary.

Sources:
- Team framework: https://github.com/kenaucrebot/2026/blob/main/main.py (inspected blob b593dd15a7b8e02d847afdb478111ff7dd2a2f9f)
- Team setup/reference: https://github.com/kenaucrebot/2026/blob/main/README.md
- DriveBase API: https://docs.pybricks.com/en/latest/robotics.html
- Mission scoring reference: https://www.flluae.org/assets/downloads/2.%20fll-challenge-bioglow-software-scoresheet.pdf
