"""
Execute tests for the package
"""
import sys
import unittest
import numpy as np
import timeout_decorator

sys.path.append("../0hh1")

from Solver import Solver
from SolverException import SolverException

class TestSolver(unittest.TestCase):
    """
    Test class for unittest
    """

    def test_invalid_ctor(self):
        """
        Test the object creation with invalid input
        """

        self.assertRaises(SolverException, Solver, 'NOTHING')
        self.assertRaises(SolverException, Solver, np.array(['1', 0, 0, 1]))
        self.assertRaises(SolverException, Solver, 1)

        obj = np.array([
            [1, 0, 0, 2],
            [2, 0, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 3]
        ])

        # array with one invalid number
        self.assertRaises(SolverException, Solver, obj)

    def test_solved(self):
        """
        Test solved method when input is solved
        """

        obj = Solver(np.array([
            [2, 1, 1, 2],
            [1, 1, 2, 2],
            [1, 2, 2, 1],
            [2, 2, 1, 1]
        ]))
        self.assertTrue(obj.solved())  # normal 4x4 solved

    def test_unsolved(self):
        """
        Test solved method when input is unsolved
        """

        obj = Solver(np.array([
            [2, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 2, 0]
        ]))
        self.assertFalse(obj.solved())  # empty spaces

        obj = Solver(np.array([
            [2, 2, 2, 1, 1, 1],
            [2, 2, 2, 1, 1, 1],
            [1, 1, 1, 2, 2, 2],
            [1, 1, 1, 2, 2, 2],
            [2, 2, 2, 1, 1, 1],
            [2, 2, 2, 1, 1, 1]
        ]))
        self.assertFalse(obj.solved())  # equal rows and columns

    @timeout_decorator.timeout(30)
    def test_solve(self):
        """
        Test solve method
        """

        obj = Solver(np.array([
            [2, 0, 2, 0],
            [0, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 2, 0]
        ]))

        completed = np.array([
            [2, 1, 2, 1],
            [1, 2, 1, 2],
            [2, 1, 1, 2],
            [1, 2, 2, 1]
        ])

        self.assertTrue((obj.solve()==completed).all())  # solve 4x4 unsolved input

        obj = Solver(np.array([
            [0, 0, 1, 1, 0, 0],
            [0, 2, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 1],
            [2, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 0],
            [0, 0, 0, 2, 0, 0]
        ]))

        completed = np.array([
            [1, 2, 1, 1, 2, 2],
            [1, 2, 2, 1, 1, 2],
            [2, 1, 1, 2, 2, 1],
            [2, 2, 1, 1, 2, 1],
            [1, 1, 2, 2, 1, 2],
            [2, 1, 2, 2, 1, 1]
        ])

        self.assertTrue((obj.solve()==completed).all())  # solve 6x6 unsolved input

        obj = Solver(np.array([
            [2, 0, 1, 0, 0, 2, 0, 0],
            [2, 2, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 0, 1, 0, 2, 0, 0],
            [2, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 2, 2, 0],
            [0, 0, 0, 2, 0, 0, 0, 0]
        ]))

        completed = np.array([
            [2, 2, 1, 1, 2, 2, 1, 1],
            [2, 2, 1, 2, 1, 1, 2, 1],
            [1, 1, 2, 1, 2, 2, 1, 2],
            [1, 2, 1, 2, 2, 1, 1, 2],
            [2, 1, 2, 1, 1, 2, 2, 1],
            [2, 1, 2, 1, 2, 1, 1, 2],
            [1, 2, 1, 2, 1, 2, 2, 1],
            [1, 1, 2, 2, 1, 1, 2, 2]
        ])

        self.assertTrue((obj.solve()==completed).all())  # solve 8x8 unsolved input

        obj = Solver(np.array([
            [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
            [1, 0, 0, 0, 2, 0, 1, 0, 0, 0],
            [1, 1, 0, 1, 0, 0, 0, 2, 2, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0, 0, 2, 0, 2],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 2],
            [0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 2, 0, 0, 1, 0],
            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 1, 1, 0, 0]
        ]))

        completed = np.array([
            [2, 2, 1, 2, 1, 1, 2, 1, 1, 2],
            [1, 1, 2, 1, 2, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 2, 1, 2, 2, 1],
            [2, 2, 1, 2, 1, 1, 2, 1, 2, 1],
            [2, 1, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 1, 2, 1, 2, 1, 2, 2, 1, 2],
            [2, 2, 1, 1, 2, 1, 2, 1, 2, 1],
            [1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [2, 1, 2, 2, 1, 1, 2, 1, 2, 1],
            [1, 2, 2, 1, 2, 2, 1, 1, 2, 1]
        ])

        self.assertTrue((obj.solve()==completed).all())  # solve 10x10 unsolved input

        obj = Solver(np.array([
            [1, 1, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 2],
            [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 2, 0, 0, 1, 0, 0, 0, 0, 1, 0, 2],
            [0, 1, 1, 0, 0, 2, 0, 0, 2, 0, 2, 2],
            [0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 2],
            [0, 0, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0]
        ]))

        completed = np.array([
            [1, 1, 2, 2, 1, 1, 2, 2, 1, 2, 2, 1],
            [2, 2, 1, 2, 1, 1, 2, 1, 1, 2, 1, 2],
            [2, 2, 1, 1, 2, 2, 1, 1, 2, 1, 2, 1],
            [1, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2],
            [2, 2, 1, 2, 1, 2, 1, 1, 2, 1, 2, 1],
            [2, 1, 2, 1, 2, 1, 2, 2, 1, 2, 1, 1],
            [1, 2, 2, 1, 1, 2, 2, 1, 2, 1, 1, 2],
            [2, 1, 1, 2, 1, 2, 1, 1, 2, 1, 2, 2],
            [1, 2, 1, 2, 2, 1, 1, 2, 1, 2, 2, 1],
            [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 1, 2],
            [1, 1, 2, 2, 1, 2, 1, 2, 1, 2, 1, 2],
            [1, 2, 1, 1, 2, 2, 1, 2, 2, 1, 2, 1]
        ])

        self.assertTrue((obj.solve()==completed).all())  # solve 12x12 unsolved input
