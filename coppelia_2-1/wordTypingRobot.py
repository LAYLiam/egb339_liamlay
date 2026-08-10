import math
import numpy as np


def wordTypingRobot(robotObj, word: str):
    """
    Type out a word on the screen using the Dobot Robot.
    Note: You must not change the name of this file or this function.

    Parameters
    ----------
    robotObj
        Dobot object; see fakeRobot.py for the API
        You can pass in a FakeRobot or CoppeliaRobot object for testing
    word
        Word to type out

    """
    print(f"I was asked to type: {word}")

    for letter in word:
        gotoKeylocation(robotObj, letter)


# Note: The remainder of the file is a template on how we would solve this task.
# You are free to use our template, or to write your own code.
def gotoKeylocation(robotObj, letter: str):
    pos = getPositionForLetter(letter)
    jumpToPos(robotObj, pos)


def getPositionForLetter(letter: str) -> np.array:
    '''
    This function should return the x, y, z coordinates of the letter on the screen.
    You need to figure out what these coordinates are for each letter.
    '''
    pass


def jumpToPos(robotObj, target_pos: np.array):
    '''
    This function should move the robot to the given position.
    Note: We recommend the following strategy:
    1. Move the robot to a position 20mm above the target position
    2. Move the robot to the target position
    3. Move the robot to a position 20mm above the target position
    This strategy will avoid the pen to drag across the screen
    '''
    # Move the robot to a position 20mm above the target position
    pos = target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)

    # Move the robot to the target position
    pos = target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)

    # Move the robot to a position 20mm above the target position
    pos = target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)


def ikine(pos: np.array) -> np.array:
    '''
    This function should return the joint angles for the given position.
    '''
    pass
