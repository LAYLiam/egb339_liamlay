#!/usr/bin/env python

import machinevisiontoolbox as mvt
import numpy as np
import math
from typing import Tuple
import cv2

# --------- Question 1 ---------- #
def calculate_surface_area(H: np.ndarray) -> float:
    """
    Given the Homography H, return the area of the triangle with image vertices (650, 640), (580, 810), and (530, 640)
    H is defined from the image plane to the work-surface plane.
    Hint: You might find the cv2.contourArea function useful.

    Parameters
    ----------
    H
        Homography from image plane to the work-surface plane

    Returns
    -------
    float
        Area of the triangle
    """

    raise NotImplementedError("TODO: complete calculate_surface_area()")

# --------- Question 2 ---------- #
def get_image_coordinates(H: np.ndarray, Q: np.ndarray) -> np.ndarray:
    """
    Given Homography H and point Q in world coordinates, return the image
    coordinates of P (the location of Q in the image).
    H is defined from the image plane to the work-surface plane.

    Parameters
    ----------
    H
        Homography from image plane to work-surface plane
    Q
        Cartesian coordinates of point Q on the planar work-surface. Q will be numpy array of shape (2,1).

    Returns
    -------
    np.ndarray
        Cartesian coordinates of point P in image coordinates. Return as a numpy array of shape (2,1).

    """

    raise NotImplementedError("TODO: complete get_image_coordinates()")


if __name__ == "__main__":
    """
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
    pytest.main(pytest_args)"""

