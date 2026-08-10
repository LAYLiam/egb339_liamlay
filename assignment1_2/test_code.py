"""
@author: Jesse Haviland
"""

import unittest
import numpy as np
import matplotlib.pyplot as plt


class Testassignment1_2(unittest.TestCase):
    # All marks here add up to 0.0%

    # -------------- Question 1 Tests --------------- #
    def test_question_1_import(self):
        """
        Test that the rotation_matrix method can be imported
        """

        try:
            from assignment1_2 import rotation_matrix  # noqa: F401
        except ImportError:
            self.fail("Could not import rotation_matrix from assignment1_2.py")

    def test_question_1_simple(self):
        """
        Test the rotation_matrix method output
        """

        from assignment1_2 import rotation_matrix

        # test values
        axis = "x"
        angle = 0.2

        # student code
        R = rotation_matrix(axis, angle)

        if not R.shape == (3, 3):
            raise ValueError(
                f"final matrix is the incorrect size, should be (3, 3), not {R.shape}"
            )

        if R.dtype != np.float64:
            raise ValueError(
                f"The numpy array should be of type np.float64, not {R.dtype}"
            )

    # -------------- Question 2 Tests --------------- #
    def test_question_2_import(self):
        """
        Test that the using_so3 method can be imported
        """

        try:
            from assignment1_2 import using_so3  # noqa: F401
        except ImportError:
            self.fail("Could not import using_so3 from assignment1_2.py")

    def test_question_2_simple(self):
        """
        Test the using_so3 method output
        """

        from assignment1_2 import using_so3

        # student code
        result = using_so3()
        if result is None or len(result) != 3:
            raise ValueError("Function did not return the expected number of values.")
        R, p_0, q_A = result  

        if not R.shape == (3, 3):
            raise ValueError(
                f"R is the incorrect size, should be (3, 3), not {R.shape}"
            )

        if not p_0.shape == (3,):
            raise ValueError(
                f"p_0 is the incorrect size, should be (3,), not {p_0.shape}"
            )

        if not q_A.shape == (3,):
            raise ValueError(
                f"q_A is the incorrect size, should be (3,), not {q_A.shape}"
            )

        if R.dtype != np.float64:
            raise ValueError(f"R should be of type np.float64, not {R.dtype}")

        if p_0.dtype != np.float64:
            raise ValueError(f"p_0 should be of type np.float64, not {p_0.dtype}")

        if q_A.dtype != np.float64:
            raise ValueError(f"q_A should be of type np.float64, not {q_A.dtype}")

    # -------------- Question 3 Tests --------------- #
    def test_question_3_import(self):
        """
        Test that the transformation_matrix method can be imported
        """

        try:
            from assignment1_2 import transformation_matrix  # noqa: F401
        except ImportError:
            self.fail("Could not import transformation_matrix from assignment1_2.py")

    def test_question_3_simple(self):
        """
        Test the transformation_matrix method output
        """

        from assignment1_2 import transformation_matrix

        axis = "x"
        angle = 0.2
        t = np.array([4, 5, 6])
        T = transformation_matrix(axis, angle, t)

        if T is None or not isinstance(T, np.ndarray):
            raise ValueError("The function should return a numpy array")

        if not T.shape == (4, 4):
            raise ValueError(
                "Your transformation matrix is the wrong shape, should be (4, 4), not"
                f" {T.shape}"
            )

        if T.dtype != np.float64:
            raise ValueError(
                "Your transformation matrix should be of type np.float64, not"
                f" {T.dtype}"
            )

    # -------------- Question 4 Tests --------------- #
    def test_question_4_import(self):
        """
        Test that the is_se3 method can be imported
        """

        try:
            from assignment1_2 import is_se3  # noqa: F401
        except ImportError:
            self.fail("Could not import is_se3 from assignment1_2.py")

    def test_question_4_simple(self):
        """
        Test that the is_se3 returns a bool.
        """

        from assignment1_2 import is_se3  # noqa: F401
        
        true_res = is_se3(np.eye(4))
        if not isinstance(true_res,bool):
            self.fail(f"Function is_se3 must return a bool, not {type(true_res)}.")
        false_res = is_se3(np.zeros((4,4)))
        if not isinstance(false_res,bool):
            self.fail(f"Function is_se3 must return a bool, not {type(false_res)}.")

    # -------------- Question 5 Tests --------------- #
    def test_question_5_import(self):
        """
        Test that the is_se3 method can be imported
        """

        try:
            from assignment1_2 import using_se3  # noqa: F401
        except ImportError:
            self.fail("Could not import using_se3 from assignment1_2.py")

    def test_question_5_simple(self):
        """
        Test the using_se3 method output
        """

        from assignment1_2 import using_se3

        # student code
        result = using_se3()
        if result is None or len(result) != 2:
            raise ValueError("Function did not return the expected number of values.")
        p_0, q_A = result

        if not p_0.shape == (3,):
            raise ValueError(
                f"p_0 is the incorrect size, should be (3,), not {p_0.shape}"
            )

        if not q_A.shape == (3,):
            raise ValueError(
                f"q_A is the incorrect size, should be (3,), not {q_A.shape}"
            )

        if p_0.dtype != np.float64:
            raise ValueError(f"p_0 should be of type np.float64, not {p_0.dtype}")

        if q_A.dtype != np.float64:
            raise ValueError(f"q_A should be of type np.float64, not {q_A.dtype}")


if __name__ == "__main__":
    unittest.main()
