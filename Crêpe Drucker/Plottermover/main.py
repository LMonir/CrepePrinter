#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.messaging import BluetoothMailboxServer, LogicMailbox


# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()
sensor = TouchSensor(Port.S1)
motor = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)

# Write your program here.
ev3.speaker.beep()
ev3.light.on(Color.YELLOW)
motor.run(400)
while (not sensor.pressed()):
    pass
motor.stop()
ev3.light.on(Color.GREEN)
ev3.screen.clear()
ev3.screen.print('Wait for Printer', sep=' ', end='\n')
server = BluetoothMailboxServer()
server.wait_for_connection()
mbox = LogicMailbox('print', server)
ev3.screen.clear()
while True:
    mbox.wait()
    ans = mbox.read()
    ev3.light.on(Color.RED)
    if (ans):
        ev3.screen.print('Printing Mode', sep=' ', end='\n')
        motor.run_angle(-400, 3580, then=Stop.HOLD, wait=True)
        ev3.light.on(Color.YELLOW)
    else:
        ev3.screen.print('Preparation Mode', sep=' ', end='\n')
        motor.run(400)
        while (not sensor.pressed()):
            pass
        motor.stop()
        ev3.light.on(Color.GREEN)
    mbox.send(True)
    

