#!/usr/bin/env python3

import wpilib
from wpilib.drive import MecanumDrive
from networktables import NetworkTables


class MyRobot(wpilib.TimedRobot):
    """Main robot class"""

    # Channels on the roboRIO that the motor controllers are plugged in to
    frontLeftChannel = 1
    rearLeftChannel = 2
    frontRightChannel = 3
    rearRightChannel = 4

    # The channel on the driver station that the joystick is connected to
    lStickChannel = 0
    rStickChannel = 1

    def robotInit(self):
        """Robot initialization function"""
        self.frontLeftMotor = wpilib.Talon(self.frontLeftChannel)
        self.rearLeftMotor = wpilib.Talon(self.rearLeftChannel)
        self.frontRightMotor = wpilib.Talon(self.frontRightChannel)
        self.rearRightMotor = wpilib.Talon(self.rearRightChannel)
        self.speed = 0

        self.drive = MecanumDrive(
            self.frontLeftMotor,
            self.rearLeftMotor,
            self.frontRightMotor,
            self.rearRightMotor,
        )

        self.lstick = wpilib.Joystick(self.lStickChannel)
        self.rstick = wpilib.Joystick(self.rStickChannel)

        # Position gets automatically updated as robot moves
        self.gyro = wpilib.AnalogGyro(1)
        # Set game data to empty string by default
        self.gameData = ""
        # Get the SmartDashboard table from networktables
        self.sd = NetworkTables.getTable("SmartDashboard")
        self.sd.putNumber("wheelSpeed",self.speed)

    def disabled(self):
        """Called when the robot is disabled"""
        while self.isDisabled():
            wpilib.Timer.delay(0.01)

    def autonomousInit(self):
        """Called when autonomous mode is enabled"""
        self.timer = wpilib.Timer()
        self.timer.start()

    def autonomousPeriodic(self):
        if self.timer.get() < 2.0:
            self.drive.driveCartesian(0, -1, 1, 0)
        else:
            self.drive.driveCartesian(0, 0, 0, 0)

    def teleopPeriodic(self):
        """Called when operation control mode is enabled"""

        # self.drive.driveCartesian(
        #     self.lstick.getX(), -self.lstick.getY(), self.rstick.getX(), 0
        # )
        data = self.ds.getGameSpecificMessage()
        desiredSpeed = self.sd.getNumber("wheelSpeed", self.speed)
        if data:
            # Set the robot gamedata property and set a network tables value
            self.gameData = data
            self.sd.putString("gameData", self.gameData)

        self.drive.driveCartesian(
            self.lstick.getX(), -desiredSpeed, self.lstick.getRawAxis(2), 0
        )


if __name__ == "__main__":
    wpilib.run(MyRobot)
