"""
@author: Tobias Fischer, Marisa Bucolo and Jesse Haviland
"""

import unittest
from gradescope_utils.autograder_utils.decorators import (
    weight,
    number,
    visibility,
)
import os
import math
import machinevisiontoolbox as mvt
import numpy as np


class TestAssignment1_7_Q1(unittest.TestCase):
    # All marks here add up to 0.0%

    @number("Q1 Test 1")
    @weight(0)
    @visibility("visible")
    def test_question_1_import(self):
        """
        Test that the calculate_surface_area method can be imported
        """

        try:
            from assignment1_7 import calculate_surface_area  # noqa: F401
        except ImportError:
            self.fail("Could not import calculate_surface_area from assignment1_7.py")


    @number("Q1 Test 2")
    @weight(0)
    @visibility("visible")
    def test_question_1_type(self):
        """
        Test that the calculate_surface_area method returns an int or float
        """

        from assignment1_7 import calculate_surface_area

        H = np.array([[-0.8,0,0],[0,0.8,800],[0,0,2]])

        a = calculate_surface_area(H)
        if not isinstance(a, (int,float)):
            print(f"calculate_surface_area did not return an int or float")

        self.assertEqual(isinstance(a, (int,float)), True)


class TestAssignment1_7_Q2(unittest.TestCase):
    # All marks here add up to 0.0%

    @number("Q2 Test 1")
    @weight(0)
    @visibility("visible")
    def test_question_2_import(self):
        """
        Test that the get_image_coordinates method can be imported
        """

        try:
            from assignment1_7 import get_image_coordinates  # noqa: F401
        except ImportError:
            self.fail("Could not import get_image_coordinates from assignment1_7.py")


    @number("Q2 Test 2")
    @weight(0)
    @visibility("visible")
    def test_question_2_simple(self):
        """
        Test that the get_image_coordinates method returns a 2x1 matrix
        """

        from assignment1_7 import get_image_coordinates

        P = np.array([[320],[250]])
        H = np.array([[-0.8,0,0],[0,0.8,800],[0,0,2]])
        x = get_image_coordinates(H,P)
        #size should be a 2 by 1
        if x is None or not isinstance(x, np.ndarray):
            raise ValueError("The function should return a numpy array")

        s = x.shape
        if s != (2,1):
            print(f"get_image_coordinates did not return a 2x1 matrix")
            print(f"Returned: {s}")

        self.assertEqual(s, (2,1))



if __name__ == "__main__":
    unittest.main()
