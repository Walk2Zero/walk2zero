"""main.py"""
import cli_components as cli
from db_utils import DbQuery as Db

import functions.calculate_journey as calc_journey
import functions.calculate_stats as stats
import functions.login as login
import functions.menu_choices as menu


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
        # self.vehicles = {}  # not implemented due to time
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0
        
    def update_email(self, email):
        self.email = email

    # def add_vehicle(self, vehicle):
    #     self.vehicles.append(vehicle)
    #
    # def remove_vehicle(self, vehicle):
    #     self.vehicles.pop(vehicle)

    def update_user_stats(self, total_journeys, total_co2_emitted,
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
        self.carbon_emitted = None
        self.carbon_saved = None

    def update_journey_id(self):
        self.journey_id = calc_journey.get_new_journey_id(self.user_id)

    def update_datetime(self):
        self.j_datetime = calc_journey.get_datetime()

    def update_locations(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def update_journey_emissions(self, vehicle_id, carbon_emitted,
                                 carbon_saved, distance):
        self.vehicle_id = vehicle_id
        self.carbon_emitted = carbon_emitted
        self.carbon_saved = carbon_saved
        self.distance = distance



    # def update_journey_details(self, journey_id, j_datetime, origin, destination, possible_distances):
    #     self.journey_id = journey_id
    #     self.j_datetime = j_datetime
    #     self.origin = origin
    #     self.destination = destination
    #     self.possible_distances = possible_distances
    #
    # def update_vehicle_choice(self, vehicle_id, distance):
    #     self.chosen_vehicle_id = vehicle_id
    #     self.chosen_distance = distance
    #
    # def update_journey_emissions(self, carbon_emitted, carbon_saved):
    #     self.carbon_emitted = carbon_emitted
    #     self.carbon_saved = carbon_saved


# —————————————————————————————————————————————————————————————————————————————
# Main menu function
# —————————————————————————————————————————————————————————————————————————————

def main_menu(user_object):
    user = user_object
    cli.header(f"Hello {user.fname} {user.lname}!")
    cli.display_main_menu()

    selected_option = menu.main_menu_select_choice()

    # (1) Calculate a journey.
    if selected_option == 1:
        # Ideally we just want the following here:
        # cli.header("Calculate a New Journey")
        # journey = Journey(user.user_id)
        # calc_journey(journey.user_id)
        # main_menu(user)


        cli.header("Calculate a New Journey")
        journey = Journey(user.user_id)
        journey.update_journey_id()
        journey.update_datetime()
        origin, destination, distances = calc_journey.get_journey_data()
        journey.update_locations(origin, destination)
        vehicle_id, carbon_emitted, carbon_saved, distance = \
            calc_journey.get_selection(distances, journey.user_id)
        journey.update_journey_emissions(vehicle_id, carbon_emitted, carbon_saved, distance)
        # Save journey details in DB.
        Db.write_journey(journey.user_id,
                         journey.journey_id,
                         journey.j_datetime,
                         journey.origin,
                         journey.destination,
                         journey.distance,
                         journey.vehicle_id)
        Db.write_journey_emissions(journey.user_id,
                                   journey.journey_id,
                                   journey.carbon_emitted,
                                   journey.carbon_saved)

        stats.carbon_to_trees(journey.carbon_saved)

        main_menu(user)

    # (2) View user stats.
    elif selected_option == 2:
        cli.header(f"User Statistics for {user.fname} {user.lname}")
        user_stats = stats.calculate_user_stats(user.user_id)
        cli.display_user_stats(user_stats)
        main_menu(user)

    # (3) Register a new transport method to user's account.
    elif selected_option == 3:
        print("reg vehicle")
        main_menu(user)

    # (4) Log user out and return to welcome screen.
    elif selected_option == 4:
        cli.thank_you()
        user.log_out()
        return main()


# —————————————————————————————————————————————————————————————————————————————
# Main
# —————————————————————————————————————————————————————————————————————————————

def main():
    # Display welcome page.
    cli.welcome_banner()
    cli.header("Log In / Register")

    # Instantiate user.
    user = User()

    # Log In.
    email = login.get_user_email()
    if Db.check_email(email):
        user.update_email(email)
        user_dict = login.login_existing_user(email)
        user.log_in(user_dict["user_id"],
                    user_dict["fname"],
                    user_dict["lname"],
                    user_dict["pword"])
    else:
        print("\nIt looks like you are a new user.")
        user.update_email(email)
        user_dict = login.register_new_user(email)
        user.log_in(user_dict["user_id"],
                    user_dict["fname"],
                    user_dict["lname"],
                    user_dict["pword"])

        login.vehicle_reg(user_dict["user_id"])

    # Main menu (see above for main menu function).
    main_menu(user)


if __name__ == '__main__':
    main()
