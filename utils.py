"""utils.py"""
import re
from cli_components import CliComponent


# —————————————————————————————————————————————————————————————————————————————
# General Helper Functions
# —————————————————————————————————————————————————————————————————————————————

def option_to_exit(user_input):
    """Allows user to exit the program by typeing 'q' or 'Q'."""
    if user_input in ['q', 'Q']:
        CliComponent.thank_you()
        exit(0)


# —————————————————————————————————————————————————————————————————————————————
# Log In Helper Functions
# —————————————————————————————————————————————————————————————————————————————

def is_valid_email(email):
    """Checks if email address is of the correct structure."""
    regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    if re.fullmatch(regex, email):
        return True
    else:
        return False


def get_user_email():
    """Gets email address from user as text input."""
    email = input("Email address: ")
    option_to_exit(email)
    try:
        if not is_valid_email(email):
            raise ValueError
    except ValueError:
        print("\nOoops! That doesn't look like an email address.\n"
              "Please try again.\n")
        get_user_email()
    else:
        return email


def get_new_user_fname():
    fname = input("First name: ")
    option_to_exit(fname)
    try:
        if len(fname) < 2 or len(fname) > 25:
            raise ValueError
    except ValueError:
        print("First name must be 3–25 characters.\n"
              "Please try again.\n")
        get_new_user_fname()
    else:
        return fname


def get_new_user_lname():
    lname = input("Last name: ")
    option_to_exit(lname)
    try:
        if len(lname) < 2 or len(lname) > 25:
            raise ValueError
    except ValueError:
        print("Last name must be 3–25 characters.\n"
              "Please try again.\n")
        get_new_user_lname()
    else:
        return lname


def get_new_user_pword():
    pword = input("Password (3–20 alphanumeric characters): ")
    option_to_exit(pword)
    try:
        if len(pword) < 3 or len(pword) > 20 or not pword.isalnum():
            raise ValueError
    except ValueError:
        print("Password must be 3–20 alphanumeric characters.\n"
              "Please try again.\n")
        get_new_user_pword()
    else:
        return pword


# —————————————————————————————————————————————————————————————————————————————
# Journey Helper Functions
# —————————————————————————————————————————————————————————————————————————————

def get_journey_origin():
    origin = input("Enter your origin location: ")
    option_to_exit(origin)
    try:
        # Think of more/better end cases for these!
        if len(origin) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        get_journey_origin()
    else:
        return origin


def get_journey_destination():
    destination = input("Enter your origin location: ")
    option_to_exit(destination)
    try:
        # Think of more/better end cases for these!
        if len(destination) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        get_journey_destination()
    else:
        return destination

