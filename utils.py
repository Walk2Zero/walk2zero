"""utils.py"""
import re
from cli_components import CliComponent
from db_utils import DbQueryFunction as Db


# —————————————————————————————————————————————————————————————————————————————
# General Helper Functions
# —————————————————————————————————————————————————————————————————————————————
class GeneralFunction:

    @staticmethod
    def option_to_exit(user_input):
        """Allows user to exit the program by typing 'q' or 'Q'."""
        if user_input in ['q', 'Q']:
            CliComponent.thank_you()
            exit(0)


# —————————————————————————————————————————————————————————————————————————————
# Log In Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class LogInHelpFunc:

    @staticmethod
    def is_valid_email(email):
        """Checks if email address is of the correct structure."""
        regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        if re.fullmatch(regex, email):
            return True
        else:
            return False

    @staticmethod
    def get_user_email():
        """Gets email address from user as text input."""
        email = input("Email address: ")
        GeneralFunction.option_to_exit(email)
        try:
            if not LogInHelpFunc.is_valid_email(email):
                raise ValueError
        except ValueError:
            print("\nOoops! That doesn't look like an email address.\n"
                  "Please try again.\n")
            LogInHelpFunc.get_user_email()
        else:
            return email

    @staticmethod
    def login_existing_user(email):
        email = email  # think might need this for recursion, check later
        pword = input("Password: ")
        GeneralFunction.option_to_exit(pword)
        try:
            # If password does not match the one for that email in the DB
            if not Db.authenticate(email, pword):
                raise ValueError
        except ValueError:
            print("Incorrect password. Try again.\n")
            LogInHelpFunc.verify_existing_user_pword(email) # ? check this!!
        else:
            user_dict = Db.fetch_user_details(email)
            return user_dict

    @staticmethod
    def register_new_user(email):
        CliComponent.header("New User Registration")
        fname = LogInHelpFunc.get_new_user_fname()
        lname = LogInHelpFunc.get_new_user_lname()
        pword = LogInHelpFunc.get_new_user_pword()
        Db.enter_new_user(fname, lname, email, pword)
        user_id = Db.get_new_user_id(email)
        user_dict = {
            "user_id": user_id,
            "fname": fname,
            "lname": lname,
            "pword": pword
        }
        return user_dict

        self.logged_in = True
        self.main_menu()

    @staticmethod
    def get_new_user_fname():
        fname = input("First name: ")
        GeneralFunction.option_to_exit(fname)
        try:
            if len(fname) < 2 or len(fname) > 25:
                raise ValueError
        except ValueError:
            print("First name must be 3–25 characters.\n"
                  "Please try again.\n")
            LogInHelpFunc.get_new_user_fname()
        else:
            return fname

    @staticmethod
    def get_new_user_lname():
        lname = input("Last name: ")
        GeneralFunction.option_to_exit(lname)
        try:
            if len(lname) < 2 or len(lname) > 25:
                raise ValueError
        except ValueError:
            print("Last name must be 3–25 characters.\n"
                  "Please try again.\n")
            LogInHelpFunc.get_new_user_lname()
        else:
            return lname

    @staticmethod
    def get_new_user_pword():
        pword = input("Password (3–20 alphanumeric characters): ")
        GeneralFunction.option_to_exit(pword)
        try:
            if len(pword) < 3 or len(pword) > 20 or not pword.isalnum():
                raise ValueError
        except ValueError:
            print("Password must be 3–20 alphanumeric characters.\n"
                  "Please try again.\n")
            LogInHelpFunc.get_new_user_pword()
        else:
            return pword


# —————————————————————————————————————————————————————————————————————————————
# Main Menu Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class MenuHelpFunc:

    @staticmethod
    def main_menu_select_choice():
        selected_option = input("Enter option number: ")
        GeneralFunction.option_to_exit(selected_option)
        try:
            if selected_option not in ["1", "2", "3", "4"]:
                raise ValueError
        except ValueError:
            print("Ooops! Please enter an option number between 1 and 4.\n")
            MenuHelpFunc.main_menu_select_choice()
        else:
            return int(selected_option)


# —————————————————————————————————————————————————————————————————————————————
# Journey Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class JourneyHelpFunc:

    @staticmethod
    def get_journey_origin():
        origin = input("Enter your origin location: ")
        GeneralFunction.option_to_exit(origin)
        try:
            # Think of more/better end cases for these!
            if len(origin) < 2:
                raise ValueError
        except ValueError:
            print("That doesn't look right.\n"
                  "Please try again.\n")
            JourneyHelpFunc.get_journey_origin()
        else:
            return origin

    @staticmethod
    def get_journey_destination():
        destination = input("Enter your origin location: ")
        GeneralFunction.option_to_exit(destination)
        try:
            # Think of more/better end cases for these!
            if len(destination) < 2:
                raise ValueError
        except ValueError:
            print("That doesn't look right.\n"
                  "Please try again.\n")
            JourneyHelpFunc.get_journey_destination()
        else:
            return destination


# —————————————————————————————————————————————————————————————————————————————
# Stats Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class StatsHelpFunc:

    @staticmethod
    def calculate_user_stats(user_id):
        user_stats_dict = {
            "total_journeys": Db.get_total_user_journeys(user_id),
            "total_co2_emitted": Db.get_total_co2_emitted(user_id),
            "total_co2_offset": Db.get_total_co2_saved(user_id)
        }
        return user_stats_dict
