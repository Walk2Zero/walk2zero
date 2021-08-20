import unittest
from unittest import TestCase, mock
from functions.propose_mode import str_to_float, propose_modes


class TestStrToFloat(TestCase):

    def test_parsing_str(self):
        expected = {'driving': 4.7, 'walking': 4.0, 'bicycling': 5.6, 'transit': 5.2}
        result = str_to_float({'driving': '4.7 km', 'walking': '4.0 km', 'bicycling': '5.6 km', 'transit': '5.2 km'})
        self.assertEqual(expected, result)

    def test_handle_comma(self):
        expected = {'driving': 2205, 'walking': 2188, 'bicycling': 2296, 'transit': 2543}
        result = str_to_float(
            {'driving': '2,205 km', 'walking': '2,188 km', 'bicycling': '2,296 km', 'transit': '2,543 km'})
        self.assertEqual(expected, result)


class TestProposeModes(TestCase):

    @mock.patch('functions.propose_mode.str_to_float')
    def test_short_distance(self, mock_short_distance):
        mock_short_distance.return_value = {'driving': 4.7, 'walking': 4.0, 'bicycling': 5.6, 'transit': 5.2}
        expected = {'driving': 4.7, 'walking': 4.0, 'bicycling': 5.6, 'transit': 5.2}
        result = propose_modes({'driving': 4.7, 'walking': 4.0, 'bicycling': 5.6, 'transit': 5.2})
        self.assertEqual(expected, result)

    @mock.patch('functions.propose_mode.str_to_float')
    def test_long_distance(self, mock_long_distance):
        mock_long_distance.return_value = {'driving': 6.7, 'walking': 7.0, 'bicycling': 7.6, 'transit': 6.2}
        expected = {'driving': 6.7, 'bicycling': 7.6, 'transit': 6.2}
        result = propose_modes({'driving': 6.7, 'walking': 7.0, 'bicycling': 7.6, 'transit': 6.2})
        self.assertEqual(expected, result)

    @mock.patch('functions.propose_mode.str_to_float')
    def test_super_long_distance(self, mock_super_long_distance):
        mock_super_long_distance.return_value = {'driving': 2205, 'walking': 2188, 'bicycling': 2296, 'transit': 2543}
        expected = {'driving': 2205, 'transit': 2543}
        result = propose_modes({'driving': 2205, 'walking': 2188, 'bicycling': 2296, 'transit': 2543})
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
