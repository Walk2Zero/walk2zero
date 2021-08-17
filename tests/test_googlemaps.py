import unittest
from unittest import mock
from functions.googlemaps import input_locations, get_distance


class TestGoogleMaps(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=['L3 8EN', 'B3 3DH'])
    def test_input_locations(self, mock_input):
        expected = 'L3 8EN', 'B3 3DH'
        result = input_locations()
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
