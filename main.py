#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Stop
from pybricks.tools import wait
from pybricks.robotics import DriveBase
import math


class MyBase():

    def __init__(self,leftMotor:Motor,rightMotor:Motor,wheel_diameter: int | float, axle_track: int | float) -> None:
        self.axle_track=axle_track
        self.driveBase=DriveBase(leftMotor,rightMotor,wheel_diameter,axle_track)
    def getDB(self) -> DriveBase:
        return self.driveBase
    def slalom(self, _from:str,perpendicularDistance:float) -> None:
        """
        Not Perfect.
        zigzag rezomended.
        """
        smallRadius= perpendicularDistance//2
        self._fromM = 1 if _from=="right" else -1 if _from=="left" else _from
        self.driveBase.turn(-45*self._fromM)
        self.driveBase.drive_time(int(math.sqrt(perpendicularDistance**2+smallRadius**2)/2),22,4200)
        self.driveBase.turn(-45*self._fromM)
    def zigzag(self, speed:int,_from:int | str,perpendicularDistance:int | float,DBTPARA:int | float) -> None:
        """
        Goes along the hypotenuse.
        All distances are mm.
        
        :DBTPARA:distance between target point and right angle.
         
        :_from:Can be "left", "right", 1 (for right) or -1 (for left) 
        """
        self._fromM = 1 if _from=="right" else -1 if _from=="left" else _from
        DBTPARA+=(self.axle_track//2)
        hypotenus=math.sqrt(DBTPARA**2+perpendicularDistance**2)
        sineh=DBTPARA/hypotenus
        degh=math.degrees(math.asin(sineh))
        self.driveBase.turn(degh*self._fromM)
        self.driveBase.stop()
        self.driveBase.settings(straight_speed=speed,straight_acceleration=speed)
        self.driveBase.straight(hypotenus)
        self.driveBase.stop()
        self.driveBase.settings()
        self.driveBase.turn(degh*-1*self._fromM)

if __name__ =="main":
    left = Motor(Port.B)
    right = Motor(Port.C)
    BASE = MyBase(left,right,66,130)
    BASE.zigzag(200,"left",300,100)