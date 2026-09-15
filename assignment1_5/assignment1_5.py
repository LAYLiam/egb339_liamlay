#!/usr/bin/env python

import machinevisiontoolbox as mvt
import numpy as np
import math
import os
import cv2

# --------- Question 1 ---------- #
def shape_classification(area: int, perimeter: int) -> str:
    """
    Determine the type of shape (circle, square, or
    something else) from area and perimeter of a segment.

    Parameters
    ----------
    area
        Area of the segment in pixels^2
    perimeter
        Perimeter of the segment in pixels

    Returns
    -------
    str
        A string representation of the shape, either "circle", "square", or "other"
    """
    tolerance = 0.1
    if abs((perimeter/4)**2 - area) <= tolerance: return "square"
    elif abs(math.sqrt(area/math.pi) - perimeter/(2*math.pi)) <= tolerance: return "circle"
    else: return "other"


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

