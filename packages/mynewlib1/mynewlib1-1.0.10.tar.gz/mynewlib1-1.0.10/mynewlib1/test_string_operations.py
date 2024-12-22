# tests/test_string_operations.py
import unittest
from .strop import *


class TestTask(unittest.TestCase):

    def test_single_number(self):
        task = Task('5')
        self.assertEqual(task.compute(), 5.0)

    def test_addition(self):
        task = Task('2 + 3')
        self.assertEqual(task.compute(), 5.0)

    def test_subtraction(self):
        task = Task('5 - 2')
        self.assertEqual(task.compute(), 3.0)

    def test_multiplication(self):
        task = Task('3 * 4')
        self.assertEqual(task.compute(), 12.0)

    def test_division(self):
        task = Task('10 / 2')
        self.assertEqual(task.compute(), 5.0)

    def test_combined_operations(self):
        task = Task('2 + 3 * 4')
        self.assertEqual(task.compute(), 14.0)  # 3 * 4 = 12, 2 + 12 = 14

    def test_mixed_operations(self):
        task = Task('10 - 2 + 3 * 4 / 2')
        self.assertEqual(task.compute(), 14.0)  # 3 * 4 / 2 = 6, 10 - 2 + 6 = 14


if __name__ == '__main__':
    unittest.main()