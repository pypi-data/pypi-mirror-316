import unittest

def some_function():
    return False

class TestExample(unittest.TestCase):
    def test_example(self):
        result = some_function()
        self.assertTrue(result, f"Expected True, but got {result}")

if __name__ == '__main__':
    unittest.main()