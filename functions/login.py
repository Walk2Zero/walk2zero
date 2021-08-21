import re

import cli_components as cli
from db_utils import DbQuery as Db
import functions.menu_choices as menu


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
    menu.option_to_exit(email)
    try:
        if not is_valid_email(email):
            raise ValueError
    except ValueError:
        print("\nOoops! That doesn't look like an email address.\n"
              "Please try again.\n")
        return get_user_email()
    else:
        return email


def login_existing_user(email):
    pword = input("Password: ")
    menu.option_to_exit(pword)
    try:
        # If password does not match the one for that email in the DB.
        if not Db.authenticate(email, pword):
            raise ValueError
    except ValueError:
        print("Incorrect password. Try again.\n")
        return login_existing_user(email)
    else:
        user_dict = Db.fetch_user_details(email)
        return user_dict


def register_new_user(email):
    cli.header("New User Registration")
    fname = get_new_user_fname()
    lname = get_new_user_lname()
    pword = get_new_user_pword()
    Db.enter_new_user(fname, lname, email, pword)
    user_id = Db.get_new_user_id(email)
    user_dict = {
        "user_id": user_id,
        "fname": fname,
        "lname": lname,
        "pword": pword
    }
    return user_dict


def get_new_user_fname():
    fname = input("First name: ")
    menu.option_to_exit(fname)
    try:
        if len(fname) < 2 or len(fname) > 25:
            raise ValueError
    except ValueError:
        print("First name must be 3–25 characters.\n"
              "Please try again.\n")
        return get_new_user_fname()
    else:
        return fname


def get_new_user_lname():
    lname = input("Last name: ")
    menu.option_to_exit(lname)
    try:
        if len(lname) < 2 or len(lname) > 25:
            raise ValueError
    except ValueError:
        print("Last name must be 3–25 characters.\n"
              "Please try again.\n")
        return get_new_user_lname()
    else:
        return lname


def get_new_user_pword():
    pword = input("Password (3–20 alphanumeric characters): ")
    menu.option_to_exit(pword)
    try:
        if len(pword) < 3 or len(pword) > 20 or not pword.isalnum():
            raise ValueError
    except ValueError:
        print("Password must be 3–20 alphanumeric characters.\n"
              "Please try again.\n")
        return get_new_user_pword()
    else:
        return pword


# —————————————————————————————————————————————————————————————————————————————
# Vehicle Registration Functions
# —————————————————————————————————————————————————————————————————————————————

def vehicle_reg(user_id):
    # printing the menu
    all_vehicles = uv_vehicle_map(user_id)
    print("\nWhich transportation methods would you like to be considered when "
          "calculating\n your journeys?\n"
          "The following options are available:\n")
    for record in all_vehicles:
        print(record[0], record[1])
    # Converting the vehicle_ids into a list for comparison
    vehicle_ids = []
    for i in range(len(all_vehicles)):
        vehicle_ids.append(all_vehicles[i][0])

    def user_input():
        try:
            choices = [int(choices) for choices in
                       input("Enter the Vehicle ID of all the vehicles you "
                             "wish to register(e.g. 1, 2): ").split(",")]
            if all(x in vehicle_ids for x in choices):
                print("Valid Selection!")
            else:
                print("Invalid Selection. Please select again.")
                return user_input()
        except ValueError:
            print("Invalid selection. Please input again!")
            return user_input()
        else:
            for v_id in choices:
                # print(user_id, v_id) for verification
                Db.write_user_vehicles(user_id, v_id)
            print("Selection successful!")

    user_input()


def uv_vehicle_map(user_id):
    # using list comprehension to filter out all the intersection of
    # user-registered vehicles and vehicles in the DB (c,d,e)->tuple o/p for
    # vehicle db where c is v_id,d is mode, e is emissions value
    # (a, b)->tuple o/p for user-vehicle_db where a is user-id and b is
    # vehicle-id
    all_vehicles = Db.fetch_all_vehicles()
    user_vehicles = Db.fetch_user_vehicles(user_id)
    registered_vehicles = [(c, d, e) for (c, d, e) in all_vehicles for (a, b) in user_vehicles if (c == b)]
    # filter repeated tuple
    not_registered_vehicles = [sub for sub in all_vehicles if sub not in registered_vehicles]
    return not_registered_vehicles
