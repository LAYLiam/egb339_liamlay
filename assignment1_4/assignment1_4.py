#!/usr/bin/env python

import numpy as np
import scipy.optimize
import time

L0 = 138 # height of shoulder raise joint above the ground plane
L1 = 135 # length of upper arm
L2 = 147 # length of lower arm
L3 = 50  # horizontal tool displacement from wrist passive joint
L4 = -120 # vertical tool displacement from wrist passive joint

# --------- Question 1 ---------- #
def cost(theta, pstar):
    """
    Cost function for inverse kinematics

    Parameters
    ----------
    theta
        A numpy array of shape (3,) of joint angles [theta1, theta2, theta3] (radians)
    pstar
        A numpy array of shape (3,) of the desired end-effector position [x, y, z] (mm)

    Returns
    -------
    c
        A scalar value cost which is the Euclidean distance between
        forward kinematics and pstar

    """
    return np.sqrt(np.sum((a3.forward_kinematics(theta) - pstar) ** 2))

# --------- Question 2 ---------- #
def inverse_kinematics(pstar):
    """
    Inverse kinematics using optimisation

    Parameters
    ----------
    pstar
        A numpy array of shape (3,) of the desired end-effector position [x, y, z] (mm)

    Returns
    -------
    theta
        A numpy array of shape (3,) of joint angles [theta1, theta2, theta3] (radians)
    """
    guess_theta = np.array([0.0, 0.0, 0.0])
    theta = scipy.optimize.fmin(cost, guess_theta, args=(pstar,))
    return np.array(theta, dtype=np.float64)

# --------- Question 3 ---------- #
def inverse_kinematics_geom(pstar):
    """
    Inverse kinematics using geometry

    Parameters
    ----------
    pstar
        A numpy array of shape (3,) of the desired end-effector position [x, y, z] (mm)

    Returns
    -------
    theta
        A numpy array of shape (3,) of joint angles [theta1, theta2, theta3] (radians)

    """
    start = time.time() 

    x, y, z = pstar

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

    print(f"inverse_kinematics_geom took {time.time() - start} ms to run.")

    return np.array([theta1, theta2, theta3], dtype=np.float64)

if __name__ == "__main__":
    print("")
    print("Running the public tests.")
    print("To check one question, use: pixi run run_tests 1")
    print("Replace 1 with the question number.")
    import os
    import sys
    import pytest

    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pytest_args = ["-k", "not test_submitted_files", "."]
    if len(sys.argv) > 1:
        question = sys.argv[1].lower().removeprefix("q")
        if question.isdigit():
            pytest_args = ["-k", f"question_{int(question)}_", "."]
        else:
            pytest_args += sys.argv[1:]
    pytest.main(pytest_args)


class a3:
    def forward_kinematics_q(q):
        q1, q2, q3, q4 = q

        E = (
            a3.R('z', q1) @ a3.T('z', L0) @
            a3.R('y', q2) @ a3.T('z', L1) @
            a3.R('y', q3) @ a3.T('x', L2) @
            a3.R('y', q4) @ a3.T('x', L3) @
            a3.T('z', L4))

        return E[:3, 3:4].reshape(3,)

    def joint_mapping(th):
        theta1, theta2, theta3 = th

        q1 = theta1
        q2 = theta2
        q3 = theta3 - theta2
        q4 = -theta3

        return np.array([q1, q2, q3, q4], dtype=np.float64)

    def forward_kinematics(theta):
        return a3.forward_kinematics_q(a3.joint_mapping(theta))

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


check = [[-0.28380287,  1.03177633,  1.20538981],
[-0.28380287,  1.03177633,  1.20538981],
[-0.20405381,  1.05225475,  1.16235425],
[-0.20405381,  1.05225475,  1.16235425],
[-0.15055485,  1.08170383,  1.10632151],
[-0.15055485,  1.08170383,  1.10632151],
[0.29093366, 1.03307551, 1.20253377],
[0.29093366, 1.03307551, 1.20253377],
[0.21110813, 1.05329413, 1.16027129],
[0.21110813, 1.05329413, 1.16027129]]