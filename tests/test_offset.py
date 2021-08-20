import unittest
from functions.offset import offset

class TestOffset(unittest.TestCase):
    def test_offset_proposed_mode(self):
        proposed_mode={'a': 5, 'b': 5, 'c': 15.156, 'd': 100}
        chosen_mode={'d': 100}
        self.assertIsInstance(proposed_mode,dict)
        self.assertIsInstance(chosen_mode,dict)

    def test_offset_proposed_foot(self):
        proposed_mode={'a': 5, 'b': 5, 'c': 15.156, 'd': 100}
        for key in proposed_mode:
