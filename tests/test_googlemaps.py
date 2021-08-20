import unittest
from unittest import mock
from functions.googlemaps import input_locations, get_distance


class TestGoogleMaps(unittest.TestCase):

    @mock.patch('builtins.input', side_effect=["L3 8EN", "B3 3DH"])
    def test_input_locations(self, mock_input):
        expected = "L3 8EN", "B3 3DH"
        result = input_locations()
        self.assertEqual(expected, result)

    def test_google_maps_api(self):
        origin_address = 'Liverpool L3 8EN, UK'
        destination_address = 'Birmingham B2 4QA, UK'
        distances = {'driving': '161 km', 'walking': '143 km', 'bicycling': '154 km', 'transit': '143 km'}
        durations = {'driving': '1 hour 57 mins', 'walking': '1 day 5 hours', 'bicycling': '8 hours 25 mins',
                     'transit': '1 hour 53 mins'}
        expected = origin_address, destination_address, distances, durations
        result = get_distance('L3 8EN', 'B2 4QA')
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
