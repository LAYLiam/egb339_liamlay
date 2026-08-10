"""
@author: Jesse Haviland
"""

import unittest
import numpy as np
import math as m
import matplotlib.pyplot as plt
from matplotlib.pyplot import Line2D
np.random.seed(111)

class TestAssignment1_1(unittest.TestCase):
    # All marks here add up to 0.0%

    # -------------- Question 1 Tests --------------- #
    def test_question_1_import(self):
        """
        Test that the rot_mat method can be imported
        """

        try:
            from assignment1_1 import rot_mat  # noqa: F401
        except ImportError:
            self.fail("Could not import rot_mat from assignment1_1.py")

    def test_question_1_simple(self):
        """
        Test the rot_mat method works on simple data
        """

        from assignment1_1 import rot_mat

        R = rot_mat(0.3)

        if R is None or not isinstance(R, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not R.shape == (2, 2):
            raise ValueError(
                f"The rotation matrix should be 2x2, ie. shape (2,2) not {R.shape}"
            )

        if R.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type float64, not {R.dtype}"
            )

    # -------------- Question 2 Tests --------------- #
    def test_question_2_import(self):
        """
        Test that the is_so2 method can be imported
        """

        try:
            from assignment1_1 import is_so2  # noqa: F401
        except ImportError:
            self.fail("Could not import is_so2 from assignment1_1.py")

    def test_question_2_return_type(self):
        """
        Test that the is_so2 method returns a bool
        """

        from assignment1_1 import is_so2
        res = is_so2(np.zeros((2, 2)))
        if not isinstance(res, bool):
            self.fail(f"is_so2 should return a bool, not {type(res)}")

    # -------------- Question 3 Tests --------------- #
    def test_question_3_import(self):
        """
        Test that the rotate_2d method can be imported
        """

        try:
            from assignment1_1 import rotate_2d  # noqa: F401
        except ImportError:
            self.fail("Could not import rotate_2d from assignment1_1.py")

    def test_question_3_simple(self):
        """
        Test the rotate_2d method works on simple data
        """

        from assignment1_1 import rotate_2d

        bp = rotate_2d(np.array([1, 2]), 0.6)

        if bp is None or not isinstance(bp, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not bp.shape == (2,):
            raise ValueError(
                "The coordinate vector should be a 1D array with 2 elements, ie. shape"
                f" (2,) not {bp.shape}"
            )

        if bp.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type float64, not {bp.dtype}"
            )

    # -------------- Question 4 Tests --------------- #
    def test_question_4_import(self):
        """
        Test the se_in_2d method works on simple data
        """

        from assignment1_1 import se_in_2d

        x = 1
        y = 2
        theta = np.pi / 4

        T = se_in_2d(x, y, theta)

        if T is None or not isinstance(T, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not T.shape == (3, 3):
            raise ValueError("Matrix is not 3x3")

    def test_question_4_simple(self):
        """
        Test the se_in_2d method works on simple data
        """

        from assignment1_1 import se_in_2d

        T = se_in_2d(3, 4, 0.7)

        if T is None or not isinstance(T, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not T.shape == (3, 3):
            raise ValueError(
                "The homogenous transformation matrix should be a 3x3 matrix, ie. shape"
                f" (3,3) not {T.shape}"
            )

        if T.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type float64, not {T.dtype}"
            )
    def test_question_5_import(self):
        """
        Test that the transform_2d method can be imported
        """

        try:
            from assignment1_1 import transform_2d  # noqa: F401
        except ImportError:
            self.fail("Could not import transform_2d from assignment1_1.py")

    def test_question_5_simple(self):
        """
        Test the transform_2d method works on simple data
        """

        from assignment1_1 import transform_2d

        bp = transform_2d(np.array([1, 2]), np.eye(3))

        if bp is None or not isinstance(bp, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not bp.shape == (2,):
            raise ValueError(
                "The coordinate vector should be a 1D array with 2 elements, ie. shape"
                f" (2,) not {bp.shape}"
            )

        if bp.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type float64, not {bp.dtype}"
            )


if __name__ == "__main__":
    unittest.main()
