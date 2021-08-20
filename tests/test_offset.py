import unittest
from unittest import TestCase
from functions.offset import offset


class TestOffset(TestCase):

    def test_offset(self):
        result = offset({'a': 0, 'b': 0, 'c': 150, 'd': 100},
                        {'d': 100})
        expected = 50
        self.assertEqual(expected, result)

    def test_offset_zero(self):
        result = offset({'a': 0, 'b': 0, 'c': 15, 'd': 100},
                        {'d': 100})
        expected = 0
        self.assertEqual(expected, result)

    def test_return_type(self):
        result = offset({'b': 0, 'c': 151, 'd': 100},
                        {'d': 75})
        self.assertIsInstance(result, int)


if __name__ == '__main__':
    unittest.main()
