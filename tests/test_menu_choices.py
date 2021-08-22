import unittest
from unittest import TestCase, mock
from functions.menu_choices import main_menu_select_choice


class TestMainMenu(TestCase):

    def test_option_one(self):
        with mock.patch('builtins.input', side_effect=['1']):
            expected = 1
            result = main_menu_select_choice()
            self.assertEqual(expected, result)

    def test_option_two(self):
        with mock.patch('builtins.input', side_effect=['2']):
            expected = 2
            result = main_menu_select_choice()
            self.assertEqual(expected, result)

    def test_option_three(self):
        with mock.patch('builtins.input', side_effect=['3']):
            expected = 3
            result = main_menu_select_choice()
            self.assertEqual(expected, result)

    def test_option_four(self):
        with mock.patch('builtins.input', side_effect=['4']):
            expected = 4
            result = main_menu_select_choice()
            self.assertEqual(expected, result)

    @mock.patch('functions.menu_choices.main_menu_select_choice')
    def test_short_distance(self, mock_main_menu_select_choice):
        with mock.patch('builtins.input', side_effect=['5']):
            mock_main_menu_select_choice.return_value = False
            expected = False
            result = main_menu_select_choice()
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()

