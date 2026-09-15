import numpy as np
#import time

L0=138  # height of shoulder raise joint above ground plane
L1=135  # length of upper arm
L2=147  # length of lower arm
L3=60   # horizontal tool displacement from wrist passive joint
L4=-70  # vertical tool displacement from wrist passive joint

KEYBOARD_ORIGIN = np.array([248, -77.25, 0], dtype=np.float64)
KEYBOARD_Z_ROT = np.pi/2
KEY_HEIGHT, KEY_WIDTH = 11.5, 16.2
KEY_SPACER = 5.2

MAPPED_KEYS = {
    # Top row
    'A': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_SPACER, -2),
    'B': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*1 + KEY_SPACER, -2),
    'C': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*2 + KEY_SPACER, -2),
    'D': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*3 + KEY_SPACER, -2),
    'E': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*4 + KEY_SPACER, -2),
    'F': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*5 + KEY_SPACER, -2),
    'G': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*6 + KEY_SPACER, -2),
    'H': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*7 + KEY_SPACER, -2),
    'I': (-KEY_HEIGHT/2 - KEY_HEIGHT*2, KEY_WIDTH/2 + KEY_WIDTH*8 + KEY_SPACER, -2),

    # Middle row
    'J': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_SPACER, -2),
    'K': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*1 + KEY_SPACER, -2),
    'L': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*2 + KEY_SPACER, -2),
    'M': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*3 + KEY_SPACER, -2),
    'N': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*4 + KEY_SPACER, -2),
    'O': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*5 + KEY_SPACER, -2),
    'P': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*6 + KEY_SPACER, -2),
    'Q': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*7 + KEY_SPACER, -2),
    'R': (-KEY_HEIGHT/2 - KEY_HEIGHT, KEY_WIDTH/2 + KEY_WIDTH*8 + KEY_SPACER, -2),

    # Bottom row
    'S': (-KEY_HEIGHT/2, KEY_WIDTH/2, -2),
    'T': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*1, -2),
    'U': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*2, -2),
    'V': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*3, -2),
    'W': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*4, -2),
    'X': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*5, -2),
    'Y': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*6, -2),
    'Z': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*7, -2),
    'ENTER': (-KEY_HEIGHT/2, KEY_WIDTH/2 + KEY_WIDTH*8, -2),
}


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
        print(letter)

    jumpToPos(robotObj, getPositionForLetter("ENTER"))

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
    x, y, z = MAPPED_KEYS[letter]

    # Let k_p be the point in the keyboard coordinate frame
    # which denotes the position of a target key
    k_p = np.array([x, y, z, 1], dtype=np.float64)

    o_p = (Toolkit.T(
        R=Toolkit.R('z', 0),
        t=KEYBOARD_ORIGIN
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
    x, y, z = target_pos
    raised_target_pos = np.array([x, y, z + 20]) 

    # Move the robot to a position 20mm above the target position
    pos = raised_target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)
    #time.sleep(3)

    # Move the robot to the target position
    pos = target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)
    #time.sleep(3)

    # Move the robot to a position 20mm above the target position
    pos = raised_target_pos  # You will need to change this
    j1, j2, j3 = ikine(pos)
    #time.sleep(3)


def ikine(pos: np.array) -> np.array:
    '''
    This function should return the joint angles for the given position.
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

    return np.array([theta1, theta2, theta3], dtype=np.float64)


class Toolkit:
    def T(R, t):
        R[0:3, 3:4] = t.reshape(3, 1)
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