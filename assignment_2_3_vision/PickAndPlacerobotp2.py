from typing import Dict, Tuple
import numpy as np
import copy
import machinevisiontoolbox as mvt
import cv2

"""
Steps:
1. Locate each object in the image space.
2. Determine each object's colour and shape.
3. Determine a homography transformation between the image and the robot's XY plane.
4. Locate each object in the robot's XY plane.
"""

L0=138
L1=135
L2=147
L3=60
L4=-70


WSP_MARKERS = np.array([
    [117.7, 154.8],
    [297.7, 154.8],
    [297.7, -165.2],
    [117.7, -165.2]
])


def GetBlobsFromImg(
        img: mvt.Image, 
        sigma: int = 1, 
        h: int = 2, 
        thresh: float = 0.4,
        kernel: Tuple[int, int] = np.ones((3, 3)),
        filter: int = 200,
    ) -> Tuple[int, int, int]:

    img = np.power(img, np.ones(img.shape)*0.45)
    K_gauss = mvt.Kernel.Gauss(sigma, h)
    img = img.convolve(K_gauss)

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    Y = R + G + B
    
    r = np.divide(np.asarray(R), np.asarray(Y))
    g = np.divide(np.asarray(G), np.asarray(Y))
    b = np.divide(np.asarray(B), np.asarray(Y))

    def OpenClose(img: mvt.Image) -> mvt.Image:
        opened = img.open(kernel)
        closed = opened.close(kernel)
        return closed 

    red = OpenClose(r >= thresh)
    green = OpenClose(g >= thresh) 
    blue = OpenClose(b >= thresh) 

    # red.disp()
    # green.disp()
    # blue.disp(block=True)

    red_blobs = red.blobs().filter(area=filter)
    green_blobs = green.blobs().filter(area=filter)
    blue_blobs = blue.blobs().filter(area=filter)

    print("red blobs"); print(red_blobs)
    print("green blobs"); print(green_blobs)
    print("blue blobs"); print(blue_blobs)

    return red_blobs, green_blobs, blue_blobs


def GetMarkersAndPositions(blobs):
    red_blobs, green_blobs, blue_blobs = blobs

    shapes = {}
    markers = []

    # assign colour and shape to each blob
    for colour, blobs in [
            ("red", red_blobs), 
            ("green", green_blobs), 
            ("blue", blue_blobs)
        ]:
        for blob in blobs:
            if blob.circularity > 0.925:
                if colour == "red":
                    markers.append(blob)
                else:
                    shapes[f"{colour} circle"] = blob.centroid
            elif blob.circularity > 0.75:
                shapes[f"{colour} square"] = blob.centroid
            else:
                shapes[f"{colour} triangle"] = blob.centroid

    return OrderMarkers(markers), shapes


def OrderMarkers(markers):
    points = [m.centroid for m in markers]
    biggest_marker_index = np.argmax([m.area for m in markers])
    A = points[biggest_marker_index]

    x1, y1 = A
    x2, y2 = np.array(points)[:, 0], np.array(points)[:, 1]
    euclid_dist = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    C = points[np.argmax(euclid_dist)]

    midx, midy = ((C[0] - x1)/2) + x1, ((C[1] - y1)/2) + y1
    point_angle_relative_to_mid = [np.arctan2((p[1]-midy),(p[0]-midx)) for p in points]
    index_map = list(np.argsort(point_angle_relative_to_mid))
    index_A = index_map.index(biggest_marker_index)
    index_map = np.array(index_map[index_A:] + index_map[:index_A])

    return np.array(points)[index_map]


def PickAndPlaceRobot(robotObj, img: mvt.Image, target_positions: Dict):
    """
    Reposition objects to a desired location.
    Note: You must not change the name of this file or this function.

    Parameters
    ----------
    robotObj
        Dobot object; see fakeRobot.py for the API
        You can pass in a FakeRobot or CoppeliaRobot object for testing
    img
        A warped mvt image of the robot workspace.
    target_positions
        A dictionary containing the positions in the robot's XY plane that the
        objects must be placed.
    """
    im_markers, im_positions = GetMarkersAndPositions(GetBlobsFromImg(img))
    H = cv2.findHomography(im_markers, WSP_MARKERS)[0]

    print(H)
    print(im_markers)
    print(im_positions)
    print(target_positions)
    
    for shape, place_position in target_positions.items():
        x, y, w = H@np.append(im_positions[shape], 1).T
        X, Y = x/w, y/w
        pick_position = np.array([X, Y, 7.5])

        if len(place_position) == 2:
            np.append(place_position, 7.5)

        PickUp(robotObj, pick_position)
        Place(robotObj, place_position)

    return


# Note: The remainder of the file is a template on how we would solve this task.
# You are free to use our template, or to write your own code.
def PickUp(robotObj, target_pos: np.array): 
    """
    This function should move the robot to the given position and pick up
    an item if present.
    Note: We recommend the following strategy:
    1. Move the robot to a position 50mm above the target position
    2. Move the robot to the target position
    3. Activate the suction cup
    4. Move the robot to a position 50mm above the target position
    This strategy will prevent dragging the object.
    """
    # Move the robot to a position 50mm above the target position
    robotObj.set_suction_cup(0)
    pos = copy.deepcopy(target_pos)

    pos[2] = pos[2] + 65
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)

    # Move the robot to the target position
    pos = target_pos  # You will need to change this
    pj1, pj2, pj3 = ikine(pos)
    robotObj.move_arm(pj1, pj2, pj3)

    # Active suction cup
    robotObj.set_suction_cup(1)

    robotObj.move_arm(j1, j2, j3)


def Place(robotObj, target_pos: np.array):
    """
    This function should move the robot to the given position and release a
    held item if present.
    Note: We recommend the following strategy:
    1. Move the robot to a position 50mm above the target position
    2. Move the robot to the target position
    3. Release the suction cup
    4. Move the robot to a position 50mm above the target position
    This strategy will prevent dragging a held object.
    """
    # Move the robot to a position 50mm above the target position
    pos = target_pos
    pos = copy.deepcopy(target_pos)

    pos[2] = pos[2] + 65
    j1, j2, j3 = ikine(pos)
    robotObj.move_arm(j1, j2, j3)

    # Move the robot to the target position
    pj1, pj2, pj3 = ikine(target_pos)
    robotObj.move_arm(pj1, pj2, pj3)

    # Release the suction cup
    robotObj.set_suction_cup(0)

    # Move the robot to a position 50mm above the target position
    robotObj.move_arm(j1, j2, j3)


def ikine(pos: np.array) -> np.array:
    """
    Inverse kinematics using geometry

    Parameters
    ----------
    pos
        A numpy array of shape (3,) of the desired end-effector position [x, y, z] (mm)

    Returns
    -------
    theta
        A numpy array of shape (3,) of joint angles [theta1, theta2, theta3] (radians)

    """
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