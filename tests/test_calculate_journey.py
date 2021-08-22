from unittest import TestCase, main, mock

from functions.calculate_journey import *


class TestGetNewJourneyId(TestCase):

    @mock.patch("db_utils.DbQuery.get_max_journey_id")
    def test_none_return(self, mock_get_max_journey_id):
        mock_get_max_journey_id.return_value = None
        expected = 1
        result = get_new_journey_id(4)
        self.assertEqual(expected, result)

    @mock.patch("db_utils.DbQuery.get_max_journey_id")
    def test_int_return(self, mock_get_max_journey_id):
        mock_get_max_journey_id.return_value = 4
        expected = 5
        result = get_new_journey_id(4)
        self.assertEqual(expected, result)


class TestInputLocations(TestCase):

    @mock.patch("functions.calculate_journey.input_locations")
    def test_length_less_than_two_origin(self, mock_input_location):
        with mock.patch("builtins.input", side_effect=["L", "B3 3DH"]):
            mock_input_location.return_value = 0
            expected = 0
            result = input_locations()
            self.assertEqual(expected, result)

    @mock.patch("functions.calculate_journey.input_locations")
    def test_length_less_than_two_destination(self, mock_input_location):
        with mock.patch("builtins.input", side_effect=["B3 3DH", "L"]):
            mock_input_location.return_value = 0
            expected = 0
            result = input_locations()
            self.assertEqual(expected, result)

    def test_location_input_outputted(self):
        with mock.patch("builtins.input", side_effect=["B3 3DH", "L3"]):
            expected = "B3 3DH", "L3"
            result = input_locations()
            self.assertEqual(expected, result)


class TestGetDistance(TestCase):

    # @mock.patch("functions.calculate_journey.check_address")
    # def test_addresses_correct(self, mock_check_address):
    #     mock_check_address.return_value = True
    #     origin_address = "Liverpool L3 8EN, UK"
    #     destination_address = "Birmingham B2 4QA, UK"
    #     distances = {"driving": "161 km", "walking": "143 km",
    #                  "bicycling": "154 km", "transit": "143 km"}
    #     expected = origin_address, destination_address, distances
    #     result = get_distance("L3 8EN", "B2 4QA")
    #     self.assertEqual(expected, result)

    @mock.patch("functions.calculate_journey.check_address")
    @mock.patch("functions.calculate_journey.get_journey_data")
    def test_addresses_incorrect(self,
                                 mock_check_address,
                                 mock_get_journey_data):
        mock_check_address.return_value = False
        mock_get_journey_data.return_value = 0
        expected = 0
        result = get_distance("L3 8EN", "B2 4QA")
        self.assertEqual(expected, result)


class TestCheckAddress(TestCase):

    @mock.patch("functions.calculate_journey.check_address")
    def test_wrong_input(self, mock_check_address):
        with mock.patch("builtins.input", side_effect=["3"]):
            mock_check_address.return_value = 0
            origin_address = "Liverpool L3 8EN, UK"
            destination_address = "Birmingham B2 4QA, UK"
            distances = {"driving": "161 km",
                         "walking": "143 km",
                         "bicycling": "154 km",
                         "transit": "143 km"}
            expected = 0
            result = check_address(origin_address,
                                   destination_address,
                                   distances)
            self.assertEqual(expected, result)

    def test_addresses_correct(self):
        with mock.patch("builtins.input", side_effect=["1"]):
            origin_address = "Liverpool L3 8EN, UK"
            destination_address = "Birmingham B2 4QA, UK"
            distances = {"driving": "161 km",
                         "walking": "143 km",
                         "bicycling": "154 km",
                         "transit": "143 km"}
            output = check_address(origin_address,
                                   destination_address,
                                   distances)
            self.assertTrue(output)

    def test_addresses_incorrect(self):
        with mock.patch("builtins.input", side_effect=["2"]):
            origin_address = "Liverpool L3 8EN, UK"
            destination_address = "Birmingham B2 4QA, UK"
            distances = {"driving": "161 km",
                         "walking": "143 km",
                         "bicycling": "154 km",
                         "transit": "143 km"}
            output = check_address(origin_address,
                                   destination_address,
                                   distances)
            self.assertFalse(output)


class TestStrToFloat(TestCase):

    def test_parsing_str(self):
        expected = {"driving": 4.7,
                    "walking": 4.0,
                    "bicycling": 5.6,
                    "transit": 5.2}
        result = str_to_float({"driving": "4.7 km",
                               "walking": "4.0 km",
                               "bicycling": "5.6 km",
                               "transit": "5.2 km"})
        self.assertEqual(expected, result)

    def test_handle_comma(self):
        expected = {"driving": 2205,
                    "walking": 2188,
                    "bicycling": 2296,
                    "transit": 2543}
        result = str_to_float({"driving": "2,205 km",
                               "walking": "2,188 km",
                               "bicycling": "2,296 km",
                               "transit": "2,543 km"})
        self.assertEqual(expected, result)


class TestProposeModes(TestCase):

    @mock.patch("functions.calculate_journey.str_to_float")
    def test_short_distance(self, mock_short_distance):
        mock_short_distance.return_value = {"driving": 4.7,
                                            "walking": 4.0,
                                            "bicycling": 5.6,
                                            "transit": 5.2}
        expected = {"driving": 4.7,
                    "walking": 4.0,
                    "bicycling": 5.6,
                    "transit": 5.2}
        result = api_propose_modes({"driving": 4.7,
                                    "walking": 4.0,
                                    "bicycling": 5.6,
                                    "transit": 5.2})
        self.assertEqual(expected, result)

    @mock.patch("functions.calculate_journey.str_to_float")
    def test_long_distance(self, mock_long_distance):
        mock_long_distance.return_value = {"driving": 6.7,
                                           "walking": 7.0,
                                           "bicycling": 7.6,
                                           "transit": 6.2}
        expected = {"driving": 6.7, "bicycling": 7.6, "transit": 6.2}
        result = api_propose_modes({"driving": 6.7,
                                    "walking": 7.0,
                                    "bicycling": 7.6,
                                    "transit": 6.2})
        self.assertEqual(expected, result)

    @mock.patch("functions.calculate_journey.str_to_float")
    def test_super_long_distance(self, mock_super_long_distance):
        mock_super_long_distance.return_value = {"driving": 2205,
                                                 "walking": 2188,
                                                 "bicycling": 2296,
                                                 "transit": 2543}
        expected = {"driving": 2205, "transit": 2543}
        result = api_propose_modes({"driving": 2205,
                                    "walking": 2188,
                                    "bicycling": 2296,
                                    "transit": 2543})
        self.assertEqual(expected, result)


if __name__ == "__main__":
    main()
