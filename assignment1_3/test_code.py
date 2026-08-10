"""
@author: Jesse Haviland
"""

import unittest
import numpy as np


class Testassignment1_3(unittest.TestCase):
    # All marks here add up to 0.0%

    # -------------- Question 1 Tests --------------- #
    def test_question_1_import(self):
        """
        Test that the forward_kinematics_q method can be imported
        """

        try:
            from assignment1_3 import forward_kinematics_q  # noqa: F401
        except ImportError:
            self.fail("Could not import forward_kinematics_q from assignment1_3.py")

    def test_question_1_simple(self):
        """
        Test the forward_kinematics_q method works on simple data
        """

        from assignment1_3 import forward_kinematics_q

        q = np.array([0, 0, 0, 0])
        p = forward_kinematics_q(q)

        if p is None or not isinstance(p, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not p.shape == (3,):
            raise ValueError(
                f"final array is the incorrect size, should be (3,), not {p.shape}"
            )

        if p.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {p.dtype}"
            )

    # -------------- Question 2 Tests --------------- #
    def test_question_2_import(self):
        """
        Test that the joint_mapping method can be imported
        """

        try:
            from assignment1_3 import joint_mapping  # noqa: F401
        except ImportError:
            self.fail("Could not import joint_mapping from assignment1_3.py")

    def test_question_2_simple(self):
        """
        Test the joint_mapping method works on simple data
        """

        from assignment1_3 import joint_mapping

        th = np.array([0, np.pi / 4, 0])
        y = joint_mapping(th)

        if y is None or not isinstance(y, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not y.shape == (4,):
            raise ValueError(
                f"final array is the incorrect size, should be (4,), not {y.shape}"
            )

        if y.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {y.dtype}"
            )

    # -------------- Question 3 Tests --------------- #
    def test_question_3_import(self):
        """
        Test that the forward_kinematics method can be imported
        """

        try:
            from assignment1_3 import forward_kinematics  # noqa: F401
        except ImportError:
            self.fail("Could not import forward_kinematics from assignment1_3.py")

    def test_question_3_simple(self):
        """
        Test the forward_kinematics method works on simple data
        """

        from assignment1_3 import forward_kinematics

        th = np.array([0, np.pi / 4, 0])
        y = forward_kinematics(th)

        if y is None or not isinstance(y, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not y.shape == (3,):
            raise ValueError("Incorrect shape for output vector")

        if y.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {y.dtype}"
            )


if __name__ == "__main__":
    unittest.main()
