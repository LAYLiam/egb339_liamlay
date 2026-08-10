'''
You can run this file to test your code.
We have provided a CoppeliaRobot class that you can use to test your code.
The CoppeliaRobot class uses the same GenericRobotAPI as the real Dobot robot.
You must not submit this file - you only submit the wordTypingRobot.py file.
'''

import argparse

from coppeliaRobot import CoppeliaRobot
from genericRobotAPI import GenericRobotAPI
from wordTypingRobot import wordTypingRobot


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--printonly", action="store_true", help="Do not use the CoppeliaSim API; instead, print the joint angles to the console")
    args = parser.parse_args()

    if args.printonly:
        robot = GenericRobotAPI()
    else:
        robot = CoppeliaRobot()
    
    wordTypingRobot(robot, "hello")
