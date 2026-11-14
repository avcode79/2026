"""Reusable Pybricks forklift control. Confirmed attachment port: C.

Importing this file does not initialize hardware or move the forklift.
Calibrate direction/travel before use; no automatic hard-stop homing.
"""
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch, wait


class Forklift:
    def __init__(self, up_direction, raised_degrees, motor=None,
                 speed=100, timeout_ms=5000):
        # Degrees refer to the motor shaft, not lift height in millimeters.
        if up_direction not in (-1, 1):
            raise ValueError("Set up_direction to +1 or -1 after testing")
        if not isinstance(raised_degrees, (int, float)) or raised_degrees <= 0:
            raise ValueError("Set raised_degrees to the measured lift travel")
        if speed <= 0 or timeout_ms <= 0:
            raise ValueError("Speed and timeout must be positive")
        self.motor = motor if motor is not None else Motor(
            Port.C, Direction.CLOCKWISE
        )
        self.up_direction = up_direction
        self.raised_degrees = raised_degrees
        self.speed = speed
        self.timeout_ms = timeout_ms
        self._zeroed = False

    def zero_at_bottom(self):
        """Call ONLY when the forklift is already at its lowered position.

        Sets a reference; does NOT move down or detect the bottom.
        Use the same physical lowered position before each new program run.
        """
        self.motor.hold()
        self.motor.reset_angle(0)
        self._zeroed = True

    def move_to(self, height_degrees):
        """Move to an absolute lift position: 0=lowered, raised_degrees=up.

        Positive height always means upward regardless of motor direction.
        Blocks until completed; on a stall/timeout, stops and raises an error.
        """
        if not self._zeroed:
            raise RuntimeError("Position forklift at bottom and zero it first")
        if not 0 <= height_degrees <= self.raised_degrees:
            raise ValueError("Requested position is outside calibrated travel")
        timer = StopWatch()
        try:
            self.motor.run_target(
                self.speed, self.up_direction * height_degrees,
                then=Stop.HOLD, wait=False
            )
            while not self.motor.done():
                if self.motor.stalled():
                    raise RuntimeError("Forklift stalled; check the mechanism")
                if timer.time() >= self.timeout_ms:
                    raise RuntimeError("Forklift timed out; check travel/speed")
                wait(10)
        except BaseException:
            # Do not keep driving toward an unreachable target.
            # Brake is passive: support the lift if gravity can lower it.
            self.motor.brake()
            self._zeroed = False
            raise

    def raise_forklift(self):
        self.move_to(self.raised_degrees)

    def lower_forklift(self):
        self.move_to(0)

    def hold(self):
        """Actively hold the current motor position while the program runs."""
        self.motor.hold()

    def stop(self):
        """Cancel movement and passively brake. Re-zero before moving again."""
        self.motor.brake()
        self._zeroed = False
