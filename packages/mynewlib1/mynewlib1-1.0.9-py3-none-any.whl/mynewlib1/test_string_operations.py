# tests/test_string_operations.py

import unittest
from string_operations.operations import Task

class TestStringOperations(unittest.TestCase):

    def test_compute1(comments=False):
        assert Task('1+1').compute() == 2

        if comments:
            print('Compute completed')


    def test_compute2(comments=False):
        assert Task('1+1*5/5+8*8').compute() == 66

        if comments:
            print('compute correct')

if __name__ == '__main__':
    unittest.main()
