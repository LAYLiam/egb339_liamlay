#!/usr/bin/env python

import machinevisiontoolbox as mvt
import numpy as np
import math
from typing import Tuple
import os

# --------- Question 1 ---------- #
def coloured_objects(img: mvt.Image, gamma: float = 2.2, thresh: float = 0.6) -> Tuple[int, int, int]:
    """
    This function takes in an RGB image and returns the number of red, green, and blue squares.
    img
        RGB image. For testing, you can use img = mvt.Image.Read('sample_image.png')

    Returns
    -------
    Tuple[int, int, int]
        The number of red, green, and blue squares
    """
    img = np.power(img, np.ones(img.shape)*0.45)

    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]

    Y = R + G + B

    r = np.divide(np.asarray(R), np.asarray(Y))
    g = np.divide(np.asarray(G), np.asarray(Y))
    b = np.divide(np.asarray(B), np.asarray(Y))
    
    red = (r >= thresh)
    green = (g >= thresh) 
    blue = (b >= thresh) 

    return len(red.blobs()), len(green.blobs()), len(blue.blobs())

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