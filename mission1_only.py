# BIOGLOW robot: based on the team's supplied working program.
# Original framework authors: Coach Mark Smith-Guerrero,
# Kendall Painley, Ken Aucremanne.
# Starts immediately when Run is pressed. Position at the M01 launch pose.
from pybricks.hubs import PrimeHub
from pybricks.parameters import Direction, Port
from pybricks.pupdevices import Motor
from pybricks.robotics import DriveBase

hub = PrimeHub()
left_drive = Motor(Port.A, Direction.COUNTERCLOCKWISE)
right_drive = Motor(Port.B, Direction.CLOCKWISE)
drive_base = DriveBase(left_drive, right_drive, 43, 114)
drive_base.use_gyro(True)


def mission1():
    # Preserve the supplied program's actual DriveBase defaults.
    # It defined a settings helper but never called it.
    # No attachment motor movement was present in the supplied program.
    hub.speaker.beep()
    drive_base.straight(700)

# Mission 1 only: stop here, before the reverse/navigation to M11.
try:
    mission1()
finally:
    drive_base.brake()
