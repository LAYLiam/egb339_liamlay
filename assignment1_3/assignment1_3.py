#!/usr/bin/env python

import numpy as np

L0 = 138 # height of shoulder raise joint above the ground plane
L1 = 135 # length of the upper arm
L2 = 147 # length of the lower arm
L3 = 30  # horizontal tool displacement from wrist passive joint
L4 = -90 # vertical tool displacement from wrist passive joint

# --------- Question 1 ---------- #
def forward_kinematics_q(q):
    """
    Calculate the forward kinematics of the robot for a given set of joint angles

    Parameters
    ----------
    q
        A numpy array of shape (4,) of joint angles [q1, q2, q3, q4] in radians

    Returns
    -------
    p
        A numpy array of shape (3,) of the position of the end effector in the world
        frame in units of mm

    """
    q1, q2, q3, q4 = q

    E = (
        R('z', q1) @ T('z', L0) @ 
        R('y', q2) @ T('z', L1) @ 
        R('y', q3) @ T('x', L2) @ 
        R('y', q4) @ T('x', L3) @ 
        T('z', L4))

    return E[:3, 3:4].reshape(3,)

# --------- Question 2 ---------- #
def joint_mapping(th):
    """
    Map the physical joint angles to the kinematic joint angles

    Parameters
    ----------
    th
        A numpy array array of shape (3,) of physical joint angles
        [theta1, theta2, theta3] in radians

    Returns
    -------
    q
        A numpy array of shape (4,) of kinematic joint angles [q1, q2, q3, q4]
        in radians
    """
    theta1, theta2, theta3 = th

    q1 = theta1
    q2 = theta2
    q3 = theta3 - theta2
    q4 = -theta3

    return np.array([q1, q2, q3, q4], dtype=np.float64)

# --------- Question 3 ---------- #
def forward_kinematics(theta):
    """
    Calculate the forward kinematics of the robot for a given set of
    physical joint angles

    Parameters
    ----------
    theta
        A numpy array of shape (3,) of physical joint angles [theta1, theta2, theta3]
        in radians

    Returns
    -------
    p
        A numpy array of shape (3,) of the position of the end effector in the world
        frame in millimeters

    """
    return forward_kinematics_q(joint_mapping(theta))


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