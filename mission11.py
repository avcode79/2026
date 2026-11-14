"""BIOGLOW M11, called immediately after M01.

Uses the DriveBase API and A/B motor convention in kenaucrebot/2026.
Trial route supplied by the team; start at M01's actual ending pose.
No mission route or physical impact has been tested on your robot.
"""
from pybricks.parameters import Stop
from pybricks.tools import StopWatch, wait

# User-provided trial route from the end of mission 1.
# Distances are mm; turns are relative degrees (+right, -left).
# M01 must finish its attachment actions before this route starts.
# Forklift height after M01 is not specified; this script leaves it unchanged.
ROUTE = [
    ("straight", -150),  # Reverse clear of mission 1.
    ("turn", -90),       # Left 90 degrees.
    ("straight", 590),   # Latest supplied mission 1 program uses 590 mm.
    ("turn", 90),        # Right 90 degrees.
    ("straight", 250),   # Forward 250 mm.
    ("turn", 45),        # Right 45 degrees; bump straight from here.
]
SETUP_CONFIRMED = True  # Trial enabled using the team's existing hardware setup.
ENABLE_BUMP = True     # Set False to test only the route.

TRAVEL_SPEED = 150      # mm/s
TURN_RATE = 60          # degrees/s
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
        raise ValueError("Confirm robot dimensions and M01 ending pose first")
    if not route:
        raise ValueError("Enter the measured M01-to-M11 route first")
    for step in route:
        if len(step) != 2 or step[0] not in ("straight", "turn"):
            raise ValueError("Route entries must be (straight/turn, value)")
        if not isinstance(step[1], (int, float)):
            raise ValueError("Route distances/angles must be numbers")
    if route[0][0] != "straight" or route[0][1] >= 0:
        raise ValueError("First back straight clear of M01 before turning")
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


def mission11_after_mission1(db, route=None, confirmed=None, bump=None):
    """Reuse M01's existing DriveBase. Do not reinitialize motors or gyro.

    M01 must have finished all pending movements and placed the forklift
    in a position that clears the route. This function does not move the lift.
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


# Standalone practice: put robot at the EXACT agreed M01 ending pose.
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
    mission11_after_mission1(drive_base)
