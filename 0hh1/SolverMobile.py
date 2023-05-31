
import os
from PIL import Image
import numpy as np
from ppadb.device import Device
from Solver import Solver


class SolverMobile:
    solution: np.array = None

    _screen: np.array = None
    _problem: np.array = None
    _path: str = None
    _initialized: bool = False

    _COLORS = {
        (35, 65): 1,
        (200, 240): 2,
        (): 0
    }
    _TEMP_FILE = '01110011_01100011_01110010_01100101_01100101_01101110.png'

    def __init__(self, path: str = None, device: Device = None):
        if not path:
            if not device:
                return
            else:
                self._get_array_img(device=device)
        else:
            self._get_array_img(path=path)
        self._get_game()

    def print_problem(self) -> None:
        """Print the problem array"""
        # TODO: remove not
        if not self._problem:
            # TODO: print problem, not screen
            print(self._screen.shape)
            # print(self.__problem.shape)
            # print(self.__problem)
        else:
            print('Problem wasn\'t setted.')

    def get_game(self, path: str = None, device: Device = None) -> None:
        """Get game table in array

        Args:
            path (str, optional): path to the image file (if needed). Defaults to None.
        """
        self._get_array_img(path, device)
        self._get_game()

    def solve(self) -> None:
        """Solve the __problem with Solver"""
        if not self._initialized:
            # TODO: raise exception
            raise ModuleNotFoundError('Solver not initialized')
        solver = Solver(self._problem)
        self.solution = solver.solve()

    def _get_game(self) -> None:
        """Create game array"""
        # print(self.__screen)
        colors = []
        actual_color = -1
        for i in range(self._screen.shape[0]):
            for j in range(self._screen.shape[1]):
                lst = list(self._screen[i,j])

                flag = False
                for key, val in self._COLORS.items():
                    if lst[0] in range(key[0], key[-1]+1) and actual_color != val:
                        colors.append(val)
                        flag = True
                        actual_color = val
                        break
                if not flag:
                    actual_color = -1

        print(colors)
        self._init()

    def _init(self) -> None:
        self._initialized = True

    def _get_array_img(self, path: str = None, device: Device = None) -> None:
        """Get array from image"""

        file_p = None
        if path:
            if not os.path.exists(path):
                # TODO: change to raise Exception
                # raise SolverException(f'Passed path {path} is invalid')
                raise FileNotFoundError(f'The passed path {path} not exists!')
            self._path = file_p = path
        elif device:
            try:
                temp_img = device.screencap()
            except Exception as exc:
                raise ModuleNotFoundError('Erro connecting to device') from exc

            with open(self._TEMP_FILE, 'wb') as img:
                img.write(temp_img)
            file_p = self._TEMP_FILE

        img = Image.open(self._TEMP_FILE).convert('HSV')
        self._screen = np.array(img, dtype=np.uint8)
        img.close()

        if file_p != path and os.path.exists(file_p):
            os.remove(file_p)
