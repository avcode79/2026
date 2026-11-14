from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port, Stop
from pybricks.pupdevices import Motor
from pybricks.tools import StopWatch, wait

hub = PrimeHub()
lift = Motor(Port.C, Direction.CLOCKWISE)

FULL_HEIGHT = 639     # Your calibrated motor travel.
LIFT_SPEED = 100      # Motor degrees per second.
TIMEOUT_MS = 10000


def set_height(percent):
    target = FULL_HEIGHT * percent / 100
    timer = StopWatch()

    print("Moving to", percent, "%")

    try:
        lift.run_target(
            LIFT_SPEED,
            target,
            then=Stop.HOLD,
            wait=False
        )

        while not lift.done():
            if lift.stalled():
                raise RuntimeError("Forklift stalled")

            if timer.time() >= TIMEOUT_MS:
                raise RuntimeError("Forklift movement timed out")

            wait(10)

    except BaseException:
        lift.brake()
        raise

    print("Reached", percent, "%")
    hub.speaker.beep()


# IMPORTANT: forklift must already be at the calibrated bottom.
# This records its position; it does not automatically lower it.
lift.hold()
lift.reset_angle(0)

wait(1000)

set_height(50)
wait(2000)

set_height(100)
wait(2000)

set_height(50)

print("Test complete. Holding at 50%.")

# Keep the program running to maintain active holding.
while True:
    wait(100)
