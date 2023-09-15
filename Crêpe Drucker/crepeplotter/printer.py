#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import usocket as socket
import json
from socket_client import SocketClient

MAX_X = 232
MAX_Y = 264
UPCAST_X = 16
UPCAST_Y = 32
motorX = Motor(Port.B, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)
motorY = Motor(Port.C, positive_direction=Direction.COUNTERCLOCKWISE, gears=None)

class Printer:
    def __init__(self, ev3):
        self.ev3 = ev3
        self.motorX_max = 0
        self.motorY_max = 0
        self.stepX = 0
        self.stepY = 0
        self.currX = 0
        self.currY = 0

    def calibrate(self):
        # Bewege den Motor mit maximaler Geschwindigkeit
        motorX.dc(-50)
        wait(200)
        # Warte, bis der Motor sich nicht mehr bewegen kann
        while motorX.speed() != 0:
            wait(10)  # Kurze Pause

        # Motor stoppen
        motorX.stop()
        motorX.reset_angle(0)
        motorX.dc(50)
        wait(200)
        # Warte, bis der Motor sich nicht mehr bewegen kann
        while motorX.speed() != 0:
            wait(10)  # Kurze Pause

        # Motor stoppen
        motorX.brake()
        self.motorX_max = motorX.angle()-10
        motorX.run_angle(-800, self.motorX_max, then=Stop.HOLD, wait=True)

        # Bewege den Motor mit maximaler Geschwindigkeit
        motorY.dc(-50)
        wait(200)
        # Warte, bis der Motor sich nicht mehr bewegen kann
        while motorY.speed() != 0:
            wait(10)  # Kurze Pause

        # Motor stoppen
        motorY.stop()
        motorY.reset_angle(0)
        motorY.dc(50)
        wait(200)
        # Warte, bis der Motor sich nicht mehr bewegen kann
        while motorY.speed() != 0:
            wait(10)  # Kurze Pause

        # Motor stoppen
        motorY.brake()
        self.motorY_max = motorY.angle()-10
        motorY.run_angle(-800, self.motorY_max, then=Stop.HOLD, wait=True)

        self.stepX = self.motorX_max / MAX_X
        self.stepY = self.motorY_max / MAX_Y

        print(self.motorX_max, " ", self.stepX)
        print(self.motorY_max, " ", self.stepY)

    def moveTo(self, x, y):
        X = x + UPCAST_X
        Y = y + UPCAST_Y
        if X > (MAX_X-UPCAST_X):
            print("X ist zu groß: ", X)
            return
        if Y > (MAX_Y-UPCAST_Y):
            print("Y ist zu groß: ", Y)
            return
        diffX = X - self.currX
        diffY = Y - self.currY

        motorX.run_angle(800, diffX*self.stepX, then=Stop.HOLD, wait=False)
        motorY.run_angle(400, diffY*self.stepY, then=Stop.HOLD, wait=True)
        self.currX = X
        self.currY = Y

    def setPrintState(self, state):
        return

    def runGCode(self, ip, port):
        client = SocketClient(ip, port)
        while True:
            gcodes = client.next()
            for code in gcodes:
                codeParts = code.split()
                print(codeParts)
                if codeParts[0] == "G1":
                    self.moveTo(int(codeParts[1]), int(codeParts[2]))
                elif codeParts[0] == "G2":
                    self.setPrintState(int(codeParts[1]))
                elif codeParts[0] == "G3":
                    wait(int(codeParts[1]))
                elif("G4"):
                    return
            
