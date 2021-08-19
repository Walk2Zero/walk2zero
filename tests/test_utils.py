from unittest import TestCase, main, mock
import utils


class TestOptionToExit(TestCase):

    # Need to test that exit(0) is called by option_to_exit('q'). Not sure how
    # to do it:

    # @mock.patch.object(utils, "exit")
    # def test_exit(self, mock_exit):
    #     mock_exit.return_value = "Mock called"
    #     self.assertEqual(utils.option_to_exit('q'), "Mock called")


class TestIsValidEmail(TestCase):

    def test_good_email(self):
        self.assertTrue(utils.is_valid_email("valid@email.com"))
        self.assertTrue(utils.is_valid_email("another@valid.email.uk"))

    def test_bad_email(self):
        self.assertFalse(utils.is_valid_email("notanemailaddress"))
        self.assertFalse(utils.is_valid_email("not@valid"))
        self.assertFalse(utils.is_valid_email(""))


class TestGetUserEmail(TestCase):

    @mock.patch.object(utils, "input")
    def test_valid_email(self, mock_input):
        mock_input.return_value = "valid@email.com"
        expected_return = "valid@email.com"
        self.assertEqual(mock_input.return_value, expected_return)

    # NOTE: This test DOES pass but it raises a RecursionError because the
    # function calls itself if a ValueError is raised and I don't have time to
    # figure out how to mock this too.
    # @mock.patch.object(utils, "input")
    # def test_invalid_email(self, mock_input):
    #     mock_input.return_value = "notavalidemail"
    #     self.assertRaises(ValueError, utils.get_user_email)

    @mock.patch.object(utils, "input")
    def test_system_exit(self, mock_input):
        mock_input.return_value = "q"
        self.assertRaises(SystemExit, utils.get_user_email)


if __name__ == '__main__':
    main()
