# tests/test_core.py
import unittest
from tan_lib import add, subtract

class TestMathOperations(unittest.TestCase):
    
    def test_add(self):
        self.assertEqual(add(1, 2), 3)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)

if __name__ == "__main__":
    unittest.main()
