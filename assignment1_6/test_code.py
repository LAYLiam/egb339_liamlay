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
import cv2


class TestAssignment1_6_Q1(unittest.TestCase):
    # All marks here add up to 0.0%

    @number("Q1 Test 1")
    @weight(0)
    @visibility("visible")
    def test_question_1_import(self):
        """
        Test that the coloured_objects method can be imported
        """

        try:
            from assignment1_6 import coloured_objects  # noqa: F401
        except ImportError:
            self.fail("Could not import coloured_objects from assignment1_6.py")


    @number("Q1 Test 2")
    @weight(0)
    @visibility("visible")
    def test_question_1_simple(self):
        """
        Test that the coloured_objects method works for the sample image
        """

        from assignment1_6 import coloured_objects

        img_cv = cv2.imread("images/sample_image.png")
        img_cv = img_cv[...,::-1]
        img = mvt.Image(img_cv)
        result = coloured_objects(img)
        if result is None:
            raise ValueError("The function should return a tuple of the form (red, green, blue)")
        shapes = tuple(result)
        reference_shapes_manual = (42, 34, 52)

        if shapes != reference_shapes_manual:
            print("incorrect number of squares in sample_image")
            print(f"got {shapes[0]} red squares, {shapes[1]} green squares, and {shapes[2]} blue squares")
            print(f"expected {reference_shapes_manual[0]} red squares, {reference_shapes_manual[1]} green squares, and {reference_shapes_manual[2]} blue squares")

        self.assertEqual(shapes, reference_shapes_manual)


if __name__ == "__main__":
    unittest.main()
