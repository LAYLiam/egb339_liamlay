#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

# --------- Question 1 ---------- #
def rotation_matrix(axis, angle):
    """
    Compute 3D rotation matrix for a given axis and angle

    Parameters
    ----------
    axis
        the axis of rotation, as a string "x", "y" or "z"
    angle
        the angle of rotation in radians

    Returns
    -------
    R
        the SO(3) rotation matrix
    """
    if axis == "x":
        return np.array([
            [1, 0, 0],
            [0, np.cos(angle), -np.sin(angle)],
            [0, np.sin(angle), np.cos(angle)]
        ], dtype=np.float64)
    
    elif axis == "y":
        return np.array([
            [np.cos(angle), 0, np.sin(angle)],
            [0, 1, 0],
            [-np.sin(angle), 0, np.cos(angle)]
        ], dtype=np.float64)
    
    elif axis == "z":
        return np.array([
            [np.cos(angle), -np.sin(angle), 0],
            [np.sin(angle), np.cos(angle), 0],
            [0, 0, 1]
        ], dtype=np.float64)

# --------- Question 2 ---------- #
def using_so3():
    """
    Using a 3D rotation matrix

    Returns
    -------
    R
        the SO(3) rotation matrix describing the orientation of frame {A} with respect
        to the world frame
    p_0
        the coordinate vector P with respect to the world frame (1D array)
    q_A
        the coordinate vector Q with respect to the {A} frame (1D array)

    """
    R = rotation_matrix("x", 0.2) @ rotation_matrix("y", 0.3) @ rotation_matrix("z", 0.4)
    p_0 = R @ np.array([1, 2, 3]) 
    q_A = np.linalg.inv(R) @ np.array([3, 4, 1])
    return R, p_0, q_A

# --------- Question 3 ---------- #
def transformation_matrix(axis, angle, t):
    """
    Create a 3D homogeneous transformation matrix

    Parameters
    ----------
    axis
        the axis of rotation, as a string "x", "y" or "z"
    angle
        the angle of rotation in radians
    t
        the translation vector (1D array)

    Returns
    -------
    T
        the SE(3) transformation matrix
    """
    trans_mat = np.eye(4, dtype=np.float64)
    trans_mat[:3, :3] = rotation_matrix(axis, angle)
    trans_mat[:3, 3:4] = t.reshape(1, 3).T
    return trans_mat

# --------- Question 4 ---------- #
def is_se3(matrix):
    """
    Check if a given matrix is an SE(3) matrix.
    - check expected size
    - check that bottom row fits transformation matrix expectation
    - check that the rotation matrix R.T @ R equals identity matrix 3x3
    - check that the determinant of the rotation matrix is 1
    
    Parameters
    ----------
    matrix : numpy array
        The matrix to check

    Returns
    -------
    bool
        True if the matrix is an SE(3) homogeneous transformation matrix,
        False otherwise.
    """
    if not matrix.shape == (4, 4): return False 
    if not np.allclose(matrix[-1], np.array([0, 0, 0, 1])): return False

    R = matrix[:3, :3]
    return bool(
        np.allclose(R.T @ R, np.eye(3)) and
        np.linalg.det(R) == 1
    )

# --------- Question 5 ---------- #

def using_se3():
    """
    Using a 3D homogeneous transformation matrix

    Returns
    -------
    p_0
        the point P in the world frame (1D array)
    q_A
        the point Q in the A frame (1D array)
    """
    R = rotation_matrix('x', 0.2) @ rotation_matrix('y', 0.3) @ rotation_matrix('z', 0.4)
    t = np.array([7, 8, 9])

    T = np.eye(4, dtype=np.float64)
    T[:3, :3] = R
    T[:3, 3:4] = t.reshape(1, 3).T

    p_0 = (T @ np.array([1, 2, 3, 1]))[:3]

    q_A = (np.linalg.inv(T) @ np.array([3, 4, 1, 1]))[:3]

    return p_0, q_A

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

