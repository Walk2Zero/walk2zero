import unittest
from functions.tree_calculation import carbon_to_trees
from functions.offset import offset


class TestTreeCalculation(unittest.TestCase):

    def test_tree_calculation_input1(self):
        result2=offset({'a': 5, 'b': 5, 'c': 15.156, 'd': 100},{'d': 96})
        arg2=0
        self.assertGreater(result2,arg2)

    def test_tree_calculation_input2(self):
        result2 = offset({'a': 5, 'b': 5, 'c': 15.156, 'd': 100}, {'d': 96})
        self.assertIsInstance(result2,int)

    def test_tree_calculation_result(self):
         result1=carbon_to_trees(100)
         self.assertIsInstance(result1,str)



if __name__ == '__main__':
    unittest.main()
