"""BIOGLOW M11, called immediately after M06.

Uses the DriveBase API and A/B motor convention in kenaucrebot/2026.
Route distances MUST be measured from M06's actual ending pose.
No mission route or physical impact has been tested on your robot.
"""
from pybricks.parameters import Stop
from pybricks.tools import StopWatch, wait

# Fill in measured moves, in order. No guessed field coordinates.
# Each entry is ("straight", signed_mm) or ("turn", signed_degrees).
# Positive straight = forward; positive turn = right.
# Confirmed handoff: facing M06, lever pushed in, forklift at bottom,
# long black arm removed. FIRST back straight clear of M06, THEN turn.
# End square to the BACK of M11, with a measured bumper-to-model gap.
# Example FORMAT ONLY: [("straight", -120), ("turn", 90)]
ROUTE = []
SETUP_CONFIRMED = False  # Confirm ports, wheel size, clearance and M06 handoff.
ENABLE_BUMP = False     # First test route only; then enable the final bump.

TRAVEL_SPEED = 150      # mm/s
TURN_RATE = 60          # degrees/s, gentler with the long attachment
TRAVEL_ACCEL = 400      # mm/s squared
TURN_ACCEL = 250        # degrees/s squared

# +1: front bumper approaches model. -1: rear bumper approaches model.
# Choose based on actual contact geometry; route must match this choice.
BUMP_DIRECTION = 1
BUMP_SPEED = 200        # Initial test value, not a proven mission setting.
BUMP_MAX_MS = 650       # Includes approach across the gap and brief contact.
BUMP_MAX_MM = 100       # Encoder travel cap, NOT reliable contact detection.
RETREAT_MM = 60         # Verify this clears the falling cover and nearby models.


def _validate(route, confirmed, bump):
    if not confirmed:
        raise ValueError("Confirm robot dimensions and M06 ending pose first")
    if not route:
        raise ValueError("Enter the measured M06-to-M11 route first")
    for step in route:
        if len(step) != 2 or step[0] not in ("straight", "turn"):
            raise ValueError("Route entries must be (straight/turn, value)")
        if not isinstance(step[1], (int, float)):
            raise ValueError("Route distances/angles must be numbers")
    if route[0][0] != "straight" or route[0][1] >= 0:
        raise ValueError("First back straight clear of M06 before turning")
    if bump:
        if BUMP_DIRECTION not in (-1, 1):
            raise ValueError("BUMP_DIRECTION must be +1 or -1")
        if min(BUMP_SPEED, BUMP_MAX_MS, BUMP_MAX_MM, RETREAT_MM) <= 0:
            raise ValueError("Bump settings must be positive")


def _move(db, kind, value):
    """Bound a normal move so an obstruction cannot wait indefinitely."""
    speed = TRAVEL_SPEED if kind == "straight" else TURN_RATE
    timeout = 2000 + int(3000 * abs(value) / speed)
    timer = StopWatch()
    try:
        if kind == "straight":
            db.straight(value, then=Stop.BRAKE, wait=False)
        else:
            db.turn(value, then=Stop.BRAKE, wait=False)
        while not db.done():
            if db.stalled():
                raise RuntimeError("Route obstructed; stopped before bump")
            if timer.time() >= timeout:
                raise RuntimeError("Route move timed out; stopped before bump")
            wait(10)
    finally:
        db.brake()


def _bump(db):
    """Short straight drive; no slowing to a position target before contact.

    Stall is only a reason to stop, never proof that the cover opened.
    Wheel slip can reach the distance cap without moving the chassis.
    """
    start = db.distance()
    timer = StopWatch()
    reason = "time limit"
    try:
        db.drive(BUMP_DIRECTION * BUMP_SPEED, 0)
        while timer.time() < BUMP_MAX_MS:
            if abs(db.distance() - start) >= BUMP_MAX_MM:
                reason = "travel limit"
                break
            if db.stalled():
                reason = "stall"
                break
            wait(10)
    finally:
        db.brake()
    print("Bump stopped:", reason, "-- visually check the root cover")
    wait(150)
    _move(db, "straight", -BUMP_DIRECTION * RETREAT_MM)


def mission11_after_mission6(db, route=None, confirmed=None, bump=None):
    """Reuse M06's existing DriveBase. Do not reinitialize motors or gyro.

    M06 must have finished all pending movements and placed the forklift
    in its agreed travel position. This function does not move the lift.
    It finishes near M11, NOT at home. Return route is a separate task.
    """
    if route is None:
        route = ROUTE
    if confirmed is None:
        confirmed = SETUP_CONFIRMED
    if bump is None:
        bump = ENABLE_BUMP
    _validate(route, confirmed, bump)
    saved_settings = db.settings()
    db.brake()
    try:
        db.settings(TRAVEL_SPEED, TRAVEL_ACCEL, TURN_RATE, TURN_ACCEL)
        for kind, value in route:
            _move(db, kind, value)
        if bump:
            _bump(db)
        else:
            print("Route-only test complete. Bump disabled.")
    finally:
        db.brake()
        db.settings(*saved_settings)


# Standalone practice: put robot at the EXACT agreed M06 ending pose.
# When imported from another program, this section does not run.
if __name__ == "__main__":
    _validate(ROUTE, SETUP_CONFIRMED, ENABLE_BUMP)
    from pybricks.hubs import PrimeHub
    from pybricks.parameters import Direction, Port
    from pybricks.pupdevices import Motor
    from pybricks.robotics import DriveBase

    # Repository defaults ONLY: verify against your actual robot.
    WHEEL_DIAMETER = 43
    AXLE_TRACK = 114
    hub = PrimeHub()
    left_drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
    right_drive = Motor(Port.B, Direction.CLOCKWISE)
    drive_base = DriveBase(left_drive, right_drive, WHEEL_DIAMETER, AXLE_TRACK)
    drive_base.use_gyro(True)
    mission11_after_mission6(drive_base)
