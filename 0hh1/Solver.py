"""
Solver Class
"""

import logging as logger
import numpy as np
from SolverException import SolverException


class Solver:
    """
        Solver object
    """
    problem: np.array
    __solution: np.array
    __size: int
    __half: int
    __VALID_COLORS = [1, 2]
    __VALID_SIZES = [4, 6, 8, 10, 12]

    def __init__(self, initial_problem: np.array) -> None:

        if self.verify_array(initial_problem):
            self.problem = initial_problem.copy()
        else:
            raise SolverException('Invalid Array.')

        self.__size = initial_problem.shape[0]
        self.__half = int(self.__size / 2)
        self.__solution = initial_problem.copy()

    def verify_array(self, array: np.array) -> bool:
        """Check if the passed array is valid for 0hh1

        Args:
            array (np.array): array representig the 0hh1

        Returns:
            bool: True if the passed array is valid for 0hh1
        """

        # verify input type
        if type(array) != np.ndarray:
            return False

        dim = array.shape

        # verify array dimensions and array data type
        if (len(dim) != 2) or (str(array.dtype)[:3] != 'int'):
            return False

        validate = dim[0] in self.__VALID_SIZES and dim[0] == dim[-1]

        return (np.all((array == 0) | (array == 1) | (array == 2)) and validate)

    def __verify_squares_row(self, row: np.array) -> bool:
        """verify if row have the quantity of one color equals to half of size

        Args:
            row (np.array): one row array

        Returns:
            bool: true if have the exact half of each color
        """
        row_list = list(row)
        result = True

        for color in self.__VALID_COLORS:
            result = result and row_list.count(color) == self.__half

        return result

    def solved(self) -> bool:
        """Check if the array passed on constructor is solved

        Raises:
            SolverException: Exception

        Returns:
            bool: True if the array is solved for 0hh1 parameters
        """

        if self.__solution is None:
            return False

        if not self.verify_array(self.__solution):
            raise SolverException('Invalid Array.')

        # verify if exists any square different of the colors
        if np.all((self.__solution == 1) | (self.__solution == 2)):

            for array in [self.__solution, self.__solution.T]:
                for row in range(self.__size):
                    # verify if the number of the same color in row are more than the size / 2
                    if not self.__verify_squares_row(array[row]):
                        return False

                    # verify if exist any row equal to the actual row
                    for row1 in range(row+1, self.__size):
                        if (array[row] == array[row1]).all():
                            return False

                    # verify if exist any three squares of the same color
                    for index in range(self.__size-2):
                        if array[row, index] == array[row, index+1] == array[row, index+2]:
                            return False
        else:
            return False
        return True

    def __change_color(self, code: int) -> int:

        if code == 1:
            return 2
        elif code == 2:
            return 1
        else:
            raise SolverException(f"Invalid code for changing color! (color code: {code})")

    def __solve(self) -> None:

        counter = 0
        while not self.solved():
            counter += 1
            for arr in [self.__solution, self.__solution.T]:
                # iterate thru rows
                for row in range(self.__size):

                    # change rows with the number of squares with the same color = size/2
                    for i in [1, 2]:
                        if list(arr[row]).count(i) == self.__half:
                            arr[row][arr[row] == 0] = self.__change_color(i)

                    for i in range(self.__size-2):
                        # change square after two consecutives with the same color
                        if arr[row, i] == arr[row, i+1] != 0 and arr[row, i+2] == 0:
                            arr[row, i+2] = self.__change_color(arr[row, i])

                        # change square before two consecutives with the same color
                        aux_i = self.__size-i
                        if arr[row, aux_i-1] == arr[row, aux_i-2] != 0 and arr[row, aux_i-3] == 0:
                            arr[row, aux_i-3] = self.__change_color(arr[row, aux_i-1])

                        # verify exists two squares with the same color and a diff in the middle
                        elif arr[row, i] == arr[row, i+2] != 0 and arr[row, i+1] == 0:
                            arr[row, i+1] = self.__change_color(arr[row, i])

                    # search for rows that can be equal
                    for row1 in range(row+1, self.__size):
                        count = 0
                        for col in range(self.__size):
                            if arr[row,col] == arr[row1,col] != 0:
                                count += 1
                        if count == self.__size-2:
                            for col in range(self.__size):
                                if arr[row,col] == 0 != arr[row1,col]:
                                    arr[row,col] = self.__change_color(arr[row1,col])
                                elif arr[row1,col] == 0 != arr[row,col]:
                                    arr[row1,col] = self.__change_color(arr[row,col])
            logger.debug(f"\nArray after {counter} iterations:\n{self.__solution}")

    def solve(self) -> np.array:
        """Solve the problem passed on constructor

        Returns:
            np.array: return solved array
        """

        self.__solve()

        return self.__solution
