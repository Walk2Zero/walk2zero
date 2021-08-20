from unittest import TestCase, main, mock
from main import User

# NOTE: These tests for the OOP part of the program. I've tried my best in the
# time allowed but was unsure about it as we didn't cover testing in OOP.
class TestUser(TestCase):

    def setUp(self):
        self.user = User()

    # def tearDown(self):
    #     ?

    def test_init(self):
        self.assertIsNone(self.user.user_id)
        self.assertIsNone(self.user.fname)
        self.assertIsNone(self.user.lname)
        self.assertIsNone(self.user.email)
        self.assertFalse(self.user.logged_in)
        self.assertFalse(self.user.vehicles)
        self.assertFalse(self.user.total_journeys)
        self.assertFalse(self.user.total_co2_emitted)
        self.assertFalse(self.user.total_co2_offset)

# =============================================================================
# Log In / Register Tests
# =============================================================================

# I don't know how to test if a function is called.
#
#     @mock.patch.object(main, "Db.check_email")
#     def test_login_existing_user(self, mock_input):
#         mock_input.return_value = True
#         # assert calls self.verify_password()
#
#     @mock.patch.object(main, "Db.check_email")
#     def test_login_new_user(self, mock_input):
#         mock_input.return_value = False
#         # assert calls self.register()

if __name__ == '__main__':
    main()
