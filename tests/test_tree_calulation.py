import unittest
from unittest import TestCase
from functions.tree_calculation import carbon_to_trees


class TestTreeCalculation(TestCase):

    def test_small_offset(self):
        result = carbon_to_trees(870)
        expect = '14.65% of a tree'
        self.assertEqual(result, expect)

    def test_zero_offset(self):
        result = carbon_to_trees(0)
        expect = '0.00% of a tree'
        self.assertEqual(result, expect)

    def test_large_offset(self):
        result = carbon_to_trees(87000)
        expect = '14 trees'
        self.assertEqual(result, expect)

    def test_return_type(self):
        result=carbon_to_trees(100)
        self.assertIsInstance(result, str)





if __name__ == '__main__':
    unittest.main()