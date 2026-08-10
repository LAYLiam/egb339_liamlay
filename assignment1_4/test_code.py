"""
@author: Jesse Haviland
"""

import unittest
import numpy as np


class TestAssignment1_4(unittest.TestCase):
    # All marks here add up to 0.0%

    # -------------- Question 1 Tests --------------- #
    def test_question_1_import(self):
        """
        Test that the cost method can be imported
        """

        try:
            from assignment1_4 import cost  # noqa: F401
        except ImportError:
            self.fail("Could not import cost from assignment1_4.py")

    def test_question_1_simple(self):
        """
        Test the cost method works on simple data
        """

        from assignment1_4 import cost

        pstar = np.array([150.0, 150.0, 100.0])
        theta = np.array([0.0, 0.0, 0.0])

        c = cost(theta, pstar)

        if c is None or not isinstance(c, np.float64):
            raise ValueError("The function should return a scalar value of type float")

        if np.ndim(c) == 0:
            correct_shape = True
        else:
            print("cost should be a scalar value")
            correct_shape = False

        if c >= 0:
            correct_sign = True
        else:
            print("cost cannot be negative")
            correct_sign = False

        if not correct_shape or not correct_sign:
            raise ValueError("the return value must be a nonnegative scalar")

    # -------------- Question 2 Tests --------------- #
    def test_question_2_import(self):
        """
        Test that the inverse_kinematics method can be imported
        """

        try:
            from assignment1_4 import inverse_kinematics  # noqa: F401
        except ImportError:
            self.fail("Could not import inverse_kinematics from assignment1_4.py")

    def test_question_2_simple(self):
        """
        Test the inverse_kinematics method works on simple data
        """

        from assignment1_4 import inverse_kinematics

        pstar = np.array([150.0, 150.0, 100.0])

        y = inverse_kinematics(pstar)

        if y is None or not isinstance(y, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if y.shape != (3,):
            raise ValueError(
                f"final array is the incorrect size, should be (3,), not {y.shape}"
            )

        if y.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {y.dtype}"
            )

    # -------------- Question 3 Tests --------------- #
    def test_question_3_import(self):
        """
        Test that the inverse_kinematics_geom method can be imported
        """

        try:
            from assignment1_4 import inverse_kinematics_geom  # noqa: F401
        except ImportError:
            self.fail("Could not import inverse_kinematics_geom from assignment1_4.py")

    def test_question_3_simple(self):
        """
        Test the inverse_kinematics_geom method works on simple data
        """

        from assignment1_4 import inverse_kinematics_geom

        pstar = np.array([150.0, 150.0, 100.0])

        y = inverse_kinematics_geom(pstar)

        if y is None or not isinstance(y, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if y.shape != (3,):
            raise ValueError(
                f"final array is the incorrect size, should be (3,), not {y.shape}"
            )

        if y.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {y.dtype}"
            )


if __name__ == "__main__":
    unittest.main()
