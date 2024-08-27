#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from serialtalk.auto import SerialTalk

# This program requires LEGO EV3 MicroPython v2.0 or higher.
# Click "Open user guide" on the EV3 extension tab for more information.


# Create your objects here.
ev3 = EV3Brick()


# Write your program here.
ev3.speaker.beep()

st = SerialTalk(Port.S1)

print(st.call("echo", "Hello from ev3!"))

hue = 0

while 1:
    st.call("led", "i", hue)
    if Button.LEFT in ev3.buttons.pressed():
        hue += 10
    if Button.RIGHT in ev3.buttons.pressed():
        hue -= 10
    hue %= 359

