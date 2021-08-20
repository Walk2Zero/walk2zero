from cli_components import CliComponent
from datetime import datetime
from db_utils import DbQueryFunction as Db
from utils import LogInHelpFunc, MenuHelpFunc, StatsHelpFunc, JourneyHelpFunc
from utils_2 import VehicleReg, journey_functions


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
        self.carbon_emitted = None
        self.carbon_saved = None

    def get_locations(self, origin, destination):
        self.origin = origin
        self.destination = destination

    def get_date(self):
        now = datetime.now()
        self.j_datetime = now.strftime('%Y-%m-%d %H:%M:%S')

    def get_journey_emissions(self, vehicle_id, carbon_emitted, carbon_saved, distance):
        self.vehicle_id = vehicle_id
        self.carbon_emitted = carbon_emitted
        self.carbon_saved = carbon_saved
        self.distance = distance

    def get_journey_id(self, journey_id):
        j_id = Db.get_new_journey_id(self.user_id)
        if j_id is None:
            self.journey_id = 1
        else:
            self.journey_id = j_id + 1







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
        journey = Journey(user.user_id)
        journey.get_date()
        journey.get_journey_id(journey.user_id)
        origin, destination, distances = journey_functions.output_locations()
        journey.get_locations(origin, destination)
        vehicle_id, carbon_emitted, carbon_saved, distance = journey_functions.get_selection(distances, journey.user_id)
        journey.get_journey_emissions(vehicle_id, carbon_emitted, carbon_saved, distance)
        Db.write_journey(journey.user_id, journey.journey_id, journey.j_datetime, journey.origin, journey.destination,
                         journey.distance, journey.vehicle_id)
        Db.write_journey_emissions(journey.user_id, journey.journey_id, journey.carbon_emitted, journey.carbon_saved)
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

        VehicleReg.vehicle_reg(user_dict["user_id"][0][0])


    # Main menu.
    main_menu(user)


if __name__ == '__main__':
    main()




