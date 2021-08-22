import unittest
from unittest import TestCase
from functions.calculate_stats import carbon_to_trees


class TestTreeCalculation(TestCase):

    def test_small_offset(self):
        result = carbon_to_trees(870)
        expected = '14.65% of a tree'
        self.assertEqual(expected, result)

    def test_zero_offset(self):
        result = carbon_to_trees(0)
        expected = '0 tree'
        self.assertEqual(expected, result)

    def test_large_offset(self):
        result = carbon_to_trees(87000)
        expected = '14 trees'
        self.assertEqual(expected, result)

    def test_return_type(self):
        result = carbon_to_trees(100)
        self.assertIsInstance(result, str)





if __name__ == '__main__':
    unittest.main()