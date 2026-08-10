#!/usr/bin/env python

import math as m
import numpy as np
import matplotlib.pyplot as plt

# --------- Question 1 ---------- #
def rot_mat(theta):
    """
    Compute a 2D rotation matrix

    Parameters
    ----------
    theta
        the angle of rotation in radians

    Returns
    -------
    R
        the rotation as an SO(2) matrix
    """
    return np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ], dtype=np.float64)

# --------- Question 2 ---------- #
def is_so2(matrix):
    """
    Check if a given matrix is an SO(2) rotation matrix

    Condition:
    - matrix is expected shape (2, 2)
    - each column is orthogonal to all other columns 
    - the determinant is 1
    - the inverse is the same as the transpose 

    Parameters
    ----------
    matrix : numpy array
        the matrix to check

    Returns
    -------
    bool
        True if the matrix is an SO(2) rotation matrix, False otherwise
    """
    return bool(
        matrix.shape == (2, 2) and
        np.allclose(matrix.T[0] @ matrix.T[1], 0) and 
        np.linalg.det(matrix) == 1 and
        np.allclose(np.linalg.inv(matrix), matrix.T)
    )

# --------- Question 3 ---------- #
def rotate_2d(ap, theta):
    """
    Transform points between 2D rotated reference frames

    Parameters
    ----------
    ap
        the point with respect to {A} as a coordinate vector (1D array)
    theta
        the angle in radians of frame {B} with respect to frame {A}

    Returns
    -------
    bp
        the point with respect to {B} as a coordinate vector (1D array)
    """
    return rot_mat(-1*theta) @ ap

# --------- Question 4 ---------- #
def se_in_2d(x, y, theta):
    """
    Compute a 2D homogeneous transformation matrix

    Parameters
    ----------
    x
        the x coordinate of the translation
    y
        the y coordinate of the translation
    theta
        the angle of rotation in radians

    Returns
    -------
    T
        the transformation as an SE(2) matrix
    """
    trans_mat = np.array([
        [1, 0, x],
        [0, 1, y],
        [0, 0, 1]
    ], dtype=np.float64)
    trans_mat[:2, :2] = rot_mat(theta)
    return trans_mat

# --------- Question 5 ---------- #
def transform_2d(ap, T):
    """
    Transform points between 2D rotated and translated coordinate frames

    Parameters
    ----------
    ap
        the point with respect to {A} as a coordinate vector (1D array)
    T
        the transformation of frame {B} with respect to frame {A} as an SE(2) matrix

    Returns
    -------
    bp
        the point with respect to {B} as a coordinate vector (1D array)
    """
    return (np.linalg.inv(T) @ np.append(ap, 1))[:2]

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

