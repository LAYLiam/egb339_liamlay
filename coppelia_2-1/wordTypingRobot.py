import math
import numpy as np


L0 = 138  # height of shoulder raise joint above ground plane
L1 = 135  # length of upper arm
L2 = 147  # length of lower arm
L3 = 60   # horizontal tool displacement from wrist passive joint
L4 = -80  # vertical tool displacement from wrist passive joint


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

    for letter in word.upper():
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
    # Keys positions are mapped relative to the top left corner of the image
    MAPPED_KEYS = {
        'Q': (70, 80, 3), 
        'W': (100, 80, 3), 
        'E': (130, 80, 3), 
        'R': (165, 80, 3), 
        'T': (200, 80, 3), 
        'Y': (235, 80, 3), 
        'U': (270, 80, 3), 
        'I': (300, 80, 3), 
        'O': (335, 80, 3), 
        'P': (370, 80, 3), 
        'A': (75, 110, 3),
        'S': (110, 110, 3),
        'D': (140, 110, 3),
        'F': (175, 110, 3),
        'G': (210, 110, 3),
        'H': (245, 110, 3),
        'J': (275, 110, 3),
        'K': (310, 110, 3),
        'L': (340, 110, 3),
        'Z': (95, 145, 3),
        'X': (130, 145, 3),
        'C': (160, 145, 3),
        'V': (195, 145, 3),
        'B': (225, 145, 3),
        'N': (260, 145, 3),
        'M': (295, 145, 3),
        'ENTER': (450, 110, 3)
    }

    rel_pos = MAPPED_KEYS[letter]
    x, y, z = rel_pos

    # Adjust so that position is relative to center of image
    unscaled_width, unscaled_height = 487, 201
    x = x - (unscaled_width/2)
    y = (unscaled_height/2) - y

    # Image needs to be scaled down to match 120 x 290 mm scene board
    width, height = 290, 120
    x = x * (width/unscaled_width)
    y = y * (height/unscaled_height)

    # Let k_p be the point in the keyboard coordinate frame
    # which denotes the position of a target key
    k_p = np.array([x, y, z, 1], dtype=np.float64)

    o_p = (Toolkit.KSI(
        R=Toolkit.R('z', np.deg2rad(-135)),
        T=np.array([175, -150, 0])
    ) @ k_p)[:3]

    return o_p


def jumpToPos(robotObj, target_pos: np.array):
    '''
    This function should move the robot to the given position.
    Note: We recommend the following strategy:
    1. Move the robot to a position 20mm above the target position
    2. Move the robot to the target position
    3. Move the robot to a position 20mm above the target position
    This strategy will avoid the pen to drag across the screen
    '''
    import time 
    x, y, z = target_pos
    raised_target_pos = np.array([x, y, z + 20]) 

    # Move the robot to a position 20mm above the target position
    pos = raised_target_pos
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)
    time.sleep(3)

    # Move the robot to the target position
    pos = target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)
    time.sleep(3)

    # Move the robot to a position 20mm above the target position
    pos = raised_target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    time.sleep(3)

def ikine(pos: np.array) -> np.array:
    '''
    This function should return the joint angles for the given position.

    Joint limits
    -90 <= Theta1 >= 90 
      0 <= Theta2 >= 85
    -10 <= Theta3 >= 75
    '''
    x, y, z = pos

    r = np.sqrt(x**2 + y**2)

    a = r - L3
    b = L0 - z + L4
    c = np.sqrt(a**2 + b**2)

    delta = np.arctan2(a, b)
    alpha = np.arccos((L1**2 + L2**2 - c**2)/(2*L1*L2))
    beta = np.arccos((L1**2 + c**2 - L2**2)/(2*L1*c))

    theta1 = np.arctan2(y, x)
    theta2 = np.pi - beta - delta
    theta3 = np.pi - alpha - (np.pi/2 - theta2)

    print(
        np.degrees(theta1), 
        np.degrees(theta2), 
        np.degrees(theta3)
    )

    return np.array([theta1, theta2, theta3], dtype=np.float64)


class Toolkit:
    def KSI(R, T):
        R[0:3, 3:4] = T.reshape(3, 1)
        return R

    def R(axis, angle):
        if axis == "x":
            return np.array([
                [1, 0, 0, 0],
                [0, np.cos(angle), -np.sin(angle), 0],
                [0, np.sin(angle), np.cos(angle), 0],
                [0, 0, 0, 1]
            ], dtype=np.float64)

        elif axis == "y":
            return np.array([
                [np.cos(angle), 0, np.sin(angle), 0],
                [0, 1, 0, 0],
                [-np.sin(angle), 0, np.cos(angle), 0],
                [0, 0, 0, 1]
            ], dtype=np.float64)

        elif axis == "z":
            return np.array([
                [np.cos(angle), -np.sin(angle), 0, 0],
                [np.sin(angle), np.cos(angle), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ], dtype=np.float64)

    def T(axis, t):
        mat = np.eye(4, dtype=np.float64)

        if axis == 'x':
            mat[0:1, 3:4] = t

        elif axis == 'y':
            mat[1:2, 3:4] = t

        elif axis == 'z':
            mat[2:3, 3:4] = t

        return mat