import unittest
from unittest import TestCase, mock

import functions.login
from functions.login import *


class TestIsValidEmail(TestCase):

    def test_valid_email(self):
        email = "sarah@gmail.com"
        expected = True
        result = is_valid_email(email)
        self.assertEqual(expected, result)

    def test_invalid_email(self):
        email = "sarah.gmail.com"
        expected = False
        result = is_valid_email(email)
        self.assertEqual(expected, result)


class TestGetUserEmail(TestCase):

    @mock.patch('functions.login.is_valid_email')
    def test_valid_email(self, mock_is_valid_email):
        with mock.patch('builtins.input', side_effect=['sarah@gmail.com']):
            mock_is_valid_email.return_value = True
            expected = 'sarah@gmail.com'
            result = get_user_email()
            self.assertEqual(expected, result)

    @mock.patch('functions.login.is_valid_email')
    @mock.patch('functions.login.get_user_email')
    def test_invalid_email(self, mock_is_valid_email, mock_get_user_email):
        with mock.patch('builtins.input', side_effect=['sarah.gmail.com']):
            mock_is_valid_email.return_value = False
            mock_get_user_email.return_value = 0
            expected = 0
            result = get_user_email()
            self.assertEqual(expected, result)


class TestLoginExistingUser(TestCase):

    @mock.patch('db_utils.DbQuery.authenticate')
    @mock.patch('db_utils.DbQuery.fetch_user_details')
    def test_correct_password(self, mock_fetch_user_details, mock_authenticate):
        with mock.patch('builtins.input', side_effect=['password']):
            mock_authenticate.return_value = True
            mock_fetch_user_details.return_value = "user_dict"
            expected = "user_dict"
            result = login_existing_user("sarah@gmail.com")
            self.assertEqual(expected, result)

    @mock.patch('db_utils.DbQuery.authenticate')
    @mock.patch('db_utils.DbQuery.fetch_user_details')
    @mock.patch('functions.login.login_existing_user')
    def test_correct_password(self, mock_fetch_user_details, mock_authenticate, mock_login_existing_user):
        with mock.patch('builtins.input', side_effect=['password']):
            mock_authenticate.return_value = False
            mock_fetch_user_details.return_value = "user_dict"
            mock_login_existing_user.return_value = "log_in_again"
            expected = False
            result = login_existing_user("sarah@gmail.com")
            self.assertEqual(expected, result)


class TestGetNewUserFname(TestCase):

    @mock.patch("functions.login.get_new_user_fname")
    def test_fname_too_short(self, mock_get_new_user_fname):
        with mock.patch('builtins.input', side_effect=['S']):
            mock_get_new_user_fname.return_value = 0
            expected = 0
            result = get_new_user_fname()
            self.assertEqual(expected, result)

    @mock.patch("functions.login.get_new_user_fname")
    def test_fname_too_long(self, mock_get_new_user_fname):
        with mock.patch('builtins.input', side_effect=['Saraharaharaharaharaharaharaharaharaharah']):
            mock_get_new_user_fname.return_value = 0
            expected = 0
            result = get_new_user_fname()
            self.assertEqual(expected, result)

    def test_fname_correct(self):
        with mock.patch('builtins.input', side_effect=['Sarah']):
            expected = 'Sarah'
            result = get_new_user_fname()
            self.assertEqual(expected, result)


class TestGetNewUserLname(TestCase):

    @mock.patch("functions.login.get_new_user_lname")
    def test_lname_too_short(self, mock_get_new_user_lname):
        with mock.patch('builtins.input', side_effect=['S']):
            mock_get_new_user_lname.return_value = 0
            expected = 0
            result = get_new_user_lname()
            self.assertEqual(expected, result)

    @mock.patch("functions.login.get_new_user_lname")
    def test_lname_too_long(self, mock_get_new_user_lname):
        with mock.patch('builtins.input', side_effect=['Smithmithmithmithmithmithmithmithmithmith']):
            mock_get_new_user_lname.return_value = 0
            expected = 0
            result = get_new_user_lname()
            self.assertEqual(expected, result)

    def test_lname_correct(self):
        with mock.patch('builtins.input', side_effect=['Sarah']):
            expected = 'Sarah'
            result = get_new_user_lname()
            self.assertEqual(expected, result)


class TestGetNewUserPword(TestCase):

    @mock.patch("functions.login.get_new_user_pword")
    def test_pword_too_short(self, mock_get_new_user_pword):
        with mock.patch('builtins.input', side_effect=['Pa']):
            mock_get_new_user_pword.return_value = 0
            expected = 0
            result = get_new_user_pword()
            self.assertEqual(expected, result)

    @mock.patch("functions.login.get_new_user_pword")
    def test_pword_too_long(self, mock_get_new_user_pword):
        with mock.patch('builtins.input', side_effect=['passwordpasswordpasswordpasswordpassword']):
            mock_get_new_user_pword.return_value = 0
            expected = 0
            result = get_new_user_pword()
            self.assertEqual(expected, result)

    def test_pword_correct(self):
        with mock.patch('builtins.input', side_effect=['password123']):
            expected = 'password123'
            result = get_new_user_pword()
            self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
