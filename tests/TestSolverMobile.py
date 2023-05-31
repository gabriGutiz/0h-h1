
import unittest
import sys

sys.path.append('../0hh1')
from SolverMobile import SolverMobile

def test_from_image() -> None:
    mob_solver = SolverMobile(path='./test_files/phone_screen/4x4.jpg')

    mob_solver.print_problem()
    # mob_solver.solve()

def main() -> None:
    test_from_image()

class TestMobileComunication(unittest.TestCase):
    pass

if __name__ == '__main__':
    main()
