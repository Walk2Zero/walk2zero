import requests  # for google maps api
from cli_components import CliComponent
from db_utils import DbQueryFunction as Db
import utils


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

    # =========================================================================
    # User Log In / Register
    # =========================================================================

    def login(self):
        """Log in a user.

        This function calls the CLI header function to print the section
        header. It then calls get_user_email to take the user's email address
        as an input and assigns the input to self.email. Then it calls
        check_email to see if the user already exists or if they are a new
        user. If they are an existing user, it calls self.verify_password. If
        they are a new user, it call self.register.
        """
        CliComponent.header("Log In / Register")
        self.email = utils.get_user_email()
        if Db.check_email(self.email):
            self.verify_password()
        else:
            print("\nIt looks like you are a new user.")
            self.register()

    def verify_password(self):
        """Takes password input and verifies this against the database.

        This method takes a password as a user input. It calls authenticate to
        query the users table of the DB to check if the inputted password
        matches that of the user in the DB. It this is verified, it populates
        the instance attributes with the user_id, fname and lname from the DB
        and sets self.logged_in to True. Finally, it calls the main menu.
        """
        self.pword = input("Password: ")
        utils.option_to_exit(self.pword)
        try:
            # If password does not match the one for that email in the DB
            if not Db.authenticate(self.email, self.pword):
                raise ValueError
        except ValueError:
            print("Incorrect password. Try again.\n")
            self.verify_password()
        else:
            # If password matches, assign DB data to self
            user_dict = Db.fetch_user_details(self.email)
            self.user_id = user_dict["user_id"]
            self.fname = user_dict["fname"]
            self.lname = user_dict["lname"]
            self.logged_in = True
            self.main_menu()

    def register(self):
        """Registers a new user.

        This method takes fname, lname and a password as inputs and assigns
        them to self. It calls enter_new_user, which saves these to the
        database. It then gets the new user_id that was automatically
        generated on creation of the new user in the database and assigns it to
        self.user_id. Finally, it sets self.logged_in to True and calls the
        main menu.
        """
        CliComponent.header("New User Registration")
        self.fname = utils.get_new_user_fname()
        self.lname = utils.get_new_user_lname()
        self.pword = utils.get_new_user_pword()
        Db.enter_new_user(self.fname, self.lname, self.email, self.pword)
        self.user_id = Db.get_new_user_id(self.email)
        self.logged_in = True
        self.main_menu()

    # =========================================================================
    # User's Main Menu
    # =========================================================================

    def main_menu(self):
        """Retrieves user choice about which action to perform from main menu.

        This method displays the main user menu. It then accepts user input and
        for them to pick which action they want to perform and then it runs the
        corresponding function.
        """
        CliComponent.header(f"Welcome {self.fname} {self.lname}!")
        CliComponent.display_main_menu()

        def main_menu_select_choice():
            selected_option = input("Enter option number: ")
            utils.option_to_exit(selected_option)
            try:
                if selected_option == "1":
                    self.calculate_journey()
                elif selected_option == "2":
                    self.display_stats()
                elif selected_option == "3":
                    print("register vehicle function will be called here")
                    # self.register_vehicle()
                elif selected_option == "4":
                    self.logout()
                else:
                    raise ValueError
            except ValueError:
                print("Ooops! Please enter an option number between 1 and 4.\n")
                main_menu_select_choice()

        main_menu_select_choice()

    # -------------------------------------------------------------------------
    # Main Menu Option 1 – Calculate Journey
    # -------------------------------------------------------------------------

    def calculate_journey(self):
        journey = Journey(self.user_id)
        journey.input_locations()
        self.main_menu()

    # -------------------------------------------------------------------------
    # Main Menu Option 2 – Calculate User Stats
    # -------------------------------------------------------------------------

    def calculate_user_stats(self):
        """Fetches data from the database and saves as instance attributes.

        This method runs the database functions that calculate the total
        number of journeys made by a user, the total CO2e they have emitted on
        those journeys and the total amount of CO2e they have offset on those
        journeys by opting to take a transport option that emits a smaller
        volume of GHGs than their worst registered mode of transport."""
        self.total_journeys = Db.get_total_user_journeys(self.user_id)
        self.total_co2_emitted = Db.get_total_co2_emitted(self.user_id)
        self.total_co2_offset = Db.get_total_co2_saved(self.user_id)

    def display_stats(self):
        CliComponent.header(f"User Statistics for {self.fname} {self.lname}")
        self.calculate_user_stats()
        CliComponent.display_user_stats(self.total_journeys,
                                        self.total_co2_emitted,
                                        self.total_co2_offset)
        self.main_menu()

    # -------------------------------------------------------------------------
    # Main Menu Option 3 – Register Vehicle
    # -------------------------------------------------------------------------

    def register_vehicle(self):
        CliComponent.header("Register Vehicle")

        self.vehicles = Db.fetch_user_vehicles(self.user_id)

        # CliComponent.vehicle_registration_menu(user_id)
        # def get_option():
        #     option = input("Enter option number: ")
        # DB FUNCTION FOR WRITING TO DB GOES HERE.
        # NEEDS TO MATCH OPTION ENTERED WITH VEHICLE ID NUMBER.
        # Db.write_user_vehicle(user_id, vehicle_id)

    # -------------------------------------------------------------------------
    # Main Menu Option 4 – Log Out
    # -------------------------------------------------------------------------

    def logout(self):
        """Logs a user out of the system and restarts the program."""
        CliComponent.thank_you()

        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.pword = None
        self.logged_in = False
        self.vehicles.clear()
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

        CliComponent.welcome_banner()
        self.login()


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

    def input_locations(self):
        """
        This allows the user to input the locations of the origin and
        destination, assigns them to variables and returns these variables.
        """
        CliComponent.header("Enter Journey Details")
        self.origin = utils.get_journey_origin()
        self.destination = utils.get_journey_destination()
        self.get_distance()

    def get_distance(self):
        """
        This function takes the inputted origin and destination, then uses the
        google maps API to calculate the distances and duration (take out if
        not needed) of the route. These are outputted for each mode of
        transport so they are all available.
        """
        api_key = "API KEY GOES HERE"
        modes = ["driving", "walking", "bicycling", "transit"]
        distances = dict()

        try:
            for mode in modes:
                uri = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                      f'origins={self.origin}&' \
                      f'destinations={self.destination}&' \
                      f'mode={mode}&' \
                      f'key={api_key}&language=en-GB'

                response = requests.get(uri)
                output = response.json()

                origin_address = output['origin_addresses']
                destination_address = output['destination_addresses']

                for obj in output['rows']:
                    for data in obj['elements']:
                        distance = data['distance']['text']

                distances[mode] = distance

            self.origin = origin_address[0]
            self.destination = destination_address[0]
            self.distances = distances
        except:
            print("Something has gone wrong!\n "
                  "Try a new/clearer origin and destination.")
            self.input_locations()

        self.check_address()

    def check_address(self):

        # TO DO:
        #   -  see if we can move menu in print statement to cli_components
        #   -  update exit program to match those in User class

        # CliComponent.check_address_menu()
        # utils.get_check_address_input()


        option = input("Enter option number: ")

        try:
            if option in ['q', 'Q']:
                raise SystemExit
            elif option == "1":
                print("Addresses accepted")
                self.str_to_float()
            elif option == "2":
                print("Re-enter your origin and/or destination")
                self.input_locations()
            else:
                raise ValueError

        except SystemExit:
            CliComponent.thank_you()

        except ValueError:
            print("Ooops, try again.")
            self.check_address()

    def str_to_float(self):
        """
        Function to change the string distances in in the dictionary distances
        from the API and changes them into floats without "km".
        """
        for key, value in self.distances.items():
            value = value.replace(',', '')
            self.distances[key] = float(value[:-3])

        self.propose_modes()

    def propose_modes(self):
        """
        This function removes the "walking" mode, from the distances
        dictionary,if the distance of the journey is greater than 5km as will
        no longer be a viable mode of transport.
        """
        if self.distances['walking'] > 5:
            del self.distances['walking']
        if self.distances['bicycling'] > 100:
            del self.distances['bicycling']
        self.mode_mapping()

    def mode_mapping(self):
        print('Now we will map the modes')


def main():
    CliComponent.welcome_banner()
    user = User()
    # begin program
    user.login()


if __name__ == '__main__':
    main()
