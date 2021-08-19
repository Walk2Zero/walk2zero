import requests  # for google maps api
from cli_components import CliComponent
from db_utils import DbQueryFunction as Db
from utils import LogInHelpFunc, MenuHelpFunc, StatsHelpFunc, JourneyHelpFunc


# —————————————————————————————————————————————————————————————————————————————
# Classes
# —————————————————————————————————————————————————————————————————————————————

class User:

    def __init__(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.pword = None
        self.logged_in = False
        self.vehicles = {}
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

    def update_email(self, email):
        self.email = email

    def log_in(self, user_id, fname, lname, pword):
        self.logged_in = True
        self.user_id = user_id
        self.fname = fname
        self.lname = lname
        self.pword = pword

    def log_out(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.pword = None
        self.logged_in = False
        self.vehicles = {}
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

    # def add_vehicle(self, vehicle):
    #     self.vehicles.append(vehicle)
    #
    # def remove_vehicle(self, vehicle):
    #     self.vehicles.pop(vehicle)

    def update_user_stats(self,
                          total_journeys,
                          total_co2_emitted,
                          total_co2_offset):
        self.total_journeys = total_journeys
        self.total_co2_emitted = total_co2_emitted
        self.total_co2_offset = total_co2_offset


class Journey:

    def __init__(self, user_id):
        self.user_id = user_id
        self.journey_id = None
        self.j_datetime = None
        self.origin = None
        self.destination = None
        self.distance = None
        self.vehicle_id = None
        self.distances = None


# —————————————————————————————————————————————————————————————————————————————
# Functions
# —————————————————————————————————————————————————————————————————————————————

def main_menu(user_object):
    user = user_object
    CliComponent.header(f"Hello {user.fname} {user.lname}!")
    CliComponent.display_main_menu()

    selected_option = MenuHelpFunc.main_menu_select_choice()
    if selected_option == 1:
        CliComponent.header("Calculate a New Journey")

        print("plan journey")
        main_menu(user)
    elif selected_option == 2:
        CliComponent.header(f"User Statistics for {user.fname} {user.lname}")
        user_stats = StatsHelpFunc.calculate_user_stats(user.user_id)
        CliComponent.display_user_stats(user_stats)
        main_menu(user)
    elif selected_option == 3:
        print("reg vehicle")
        main_menu(user)
    elif selected_option == 4:
        user.log_out()
        return main()  # BUG: does not rerun main if it the first time the program is running


# —————————————————————————————————————————————————————————————————————————————
# Main
# —————————————————————————————————————————————————————————————————————————————

def main():
    # Display welcome page.
    CliComponent.welcome_banner()
    CliComponent.header("Log In / Register")

    # Instantiate user.
    user = User()

    # Log In.
    email = LogInHelpFunc.get_user_email()
    if Db.check_email(email):
        user.update_email(email)
        user_dict = LogInHelpFunc.login_existing_user(email)
        user.log_in(user_dict["user_id"],
                    user_dict["fname"],
                    user_dict["lname"],
                    user_dict["pword"])
    else:
        print("\nIt looks like you are a new user.")
        user.update_email(email)
        user_dict = LogInHelpFunc.register_new_user(email)
        user.log_in(user_dict["user_id"],
                    user_dict["fname"],
                    user_dict["lname"],
                    user_dict["pword"])

    # Main menu.
    main_menu(user)


if __name__ == '__main__':
    main()




