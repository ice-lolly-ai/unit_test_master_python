import unittest
import calc

class testUnit1(unittest.TestCase):
    
    def test_add(self):
        # result = calc.add(10, 20)
        self.assertEqual(calc.add(10, 20), 30)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)
        
    def test_add_1(self):
        # result = calc.add(10, 20)
        self.assertEqual(calc.add(10, 20), 30)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)
        
    def test_add_2(self):
        # result = calc.add(10, 20)
        self.assertEqual(calc.add(10, 20), 30)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)
        
    def test_add_3(self):
        self.assertEqual(calc.add(11, 10), 20)


if __name__ == '__main__':
    unittest.main()
    