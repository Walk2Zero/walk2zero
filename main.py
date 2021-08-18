import re  # for checking email address against regex
import requests  # for google maps api
from cli_components import CliStyle, CliComponent
from db_utils import DbQueryFunction as Db


class Walk2ZeroApp:

    def __init__(self):
        CliComponent.welcome_banner()

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
        This allows the user to input the locations of the origin and destination, assigns them to variables and returns
        these variables.

        :return: inputted origins and destination
        """

        @CliStyle.heading_1
        def journey_heading():
            print("Enter Journey Details")

        self.origin = input("Enter your origin location: ")
        try:
            if self.origin in ['q', 'Q']:
                raise SystemExit
        except SystemExit:
            CliComponent.thank_you()
        self.destination = input("Enter your destination: ")
        try:
            if self.destination in ['q', 'Q']:
                raise SystemExit
        except SystemExit:
            CliComponent.thank_you()
        self.get_distance()

    def get_distance(self):
        """
        This function takes the inputted origin and destination, then uses the google maps API to calculate the distances
        and duration (take out if not needed) of the route. These are outputted for each mode of transport so they are all
        available.

        :param origin: inputted origin
        :type origin: string
        :param destination: inputted destination
        :type destination: string
        :return: origin address, destination address and distances & durations of route for each mode of transport.
        """
        api_key = "API key"
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
            print("Something has gone wrong! \n Try a new/clearer origin and destination.")
            self.input_locations()

        self.check_address()

    def check_address(self):
        print(f'Your origin address is: {self.origin}, \n'
              f'Your origin address is: {self.destination}. \n'
              f'Please select from the following options:\n'
              f'    (1) Address shown are correct. \n'
              f'    (2) Change Addresses \n')

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
        Function to change the string distances in in the dictionary distances from the API and changes them into floats
        without "km".

        :param distances: distances as dictionary (as would be received from the function get_distance())
        :return: distances as dictionary where the values are floats of the distance (km)
        """
        for key, value in self.distances.items():
            value = value.replace(',', '')
            self.distances[key] = float(value[:-3])

        self.propose_modes()

    def propose_modes(self):
        """
        This function removes the "walking" mode, from the distances dictionary,if the distance of the journey is greater
        than 5km as will no longer be a viable mode of transport.

        :param distances: distances as dictionary (as would be received from the function get_distance())
        :return: distances as dictionary only including the viable modes of transport
        """
        if self.distances['walking'] > 5:
            del self.distances['walking']
        if self.distances['bicycling'] > 100:
            del self.distances['bicycling']
        self.mode_mapping()

    def mode_mapping(self):
        print('Now we will map the modes')

class User:

    def __init__(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.logged_in = False
        self.vehicles = []  # list of vehicle_id numbers
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0


    def login(self):
        """Log in a user.

        This method takes an email address as a user input. It assigns this to
        self.email and calls check_email to see if the email address is already
        in the DB. If the email address is already in the DB, it will run the
        self.verify_password method. If the email address is not in the
        database, it will run the self.register method.
        """
        @CliStyle.heading_1
        def login_heading():
            print("Log In / Register")

        self.email = input("Email address: ")  # try with oparry@gemail.com

        try:
            # option to quit program
            if self.email in ['q', 'Q']:
                raise SystemExit

            # if email address is not of correct structure
            regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            if re.fullmatch(regex, self.email) is None:
                raise ValueError

        except ValueError:
            print("Ooops, that doesn't look like an email address.\n"
                  "Please try again.\n")
            self.login()

        except SystemExit:
            CliComponent.thank_you()

        else:
            if Db.check_email(self.email):
                # print("Thank you. You are already registered.")
                self.verify_password()
            else:
                print("\nIt looks like you are a new user.")
                self.register()


    def verify_password(self):
        """Takes password input and verifies this against the database.

        This method takes a password as a user input. It calls authenticate to
        query the users table of the DB to check if the inputted password
        matches that of the user in the DB. It this is verified, it populates
        the object attributes with the user_id, fname and lname from the DB.
        """
        pword = input("Password: ")  # not stored to self for security

        try:
            if pword in ['q', 'Q']:
                raise SystemExit

            if Db.authenticate(self.email, pword):
                user_dict = Db.fetch_user_details(self.email)
                self.user_id = user_dict["user_id"]
                self.fname = user_dict["fname"]
                self.lname = user_dict["lname"]
                self.logged_in = True
                self.main_menu()
            else:
                raise ValueError

        except SystemExit:
            CliComponent.thank_you()

        except ValueError:
            print("Incorrect password. Try again.")
            self.verify_password()


    def register(self):
        """Registers a new user.

        This method takes fname, lname and a password as inputs and assigns
        them to self. It calls new_user, which saves these to the database.
        Finally, it sets self.logged_in to True.
        """
        @CliStyle.heading_1
        def reg_message():
            print("New User Registration")

        try:
            self.fname = input("First name: ")
            if self.fname in ['q', 'Q']:
                raise SystemExit
            if len(self.fname) < 2 or len(self.fname) > 25:
                raise ValueError

            self.lname = input("Last name: ")
            if self.lname in ['q', 'Q']:
                raise SystemExit
            if len(self.lname) < 2 or len(self.lname) > 25:
                raise ValueError

            pword = input("Password (3–20 alphanumeric characters): ")
            if pword in ['q', 'Q']:
                raise SystemExit
            if len(pword) < 3 or len(pword) > 20 or not pword.isalnum():
                raise ValueError

        except SystemExit:
            CliComponent.thank_you()

        except ValueError:
            print("Ooops, that value isn't accepted.\n"
                  "Please try registering again.\n")
            self.register()

        else:
            Db.new_user(self.fname, self.lname, self.email, pword)
            self.user_id = Db.get_new_user_id(self.email)
            self.logged_in = True
            self.main_menu()


    def main_menu(self):
        """Retrieves user choice about which action to perform from main menu.

        This method displays the main user menu. It then accepts user input and
        for them to pick which action they want to perform and then it runs the
        corresponding function.
        """

        @CliStyle.heading_1
        def user_menu_message():
            print(f"Welcome {self.fname}!")

        CliComponent.display_main_menu()

        # NOTE: I would like to put this function definition elsewhere but not
        # sure where it would go. Maybe a new python file with other similar
        # functions.
        def get_option():
            option = input("Enter option number: ")

            try:
                if option in ['q', 'Q']:
                    raise SystemExit
                elif option == "1":
                    self.calculate_journey()
                elif option == "2":
                    self.display_stats()
                elif option == "3":
                    print("register vehicle function is called here")
                    # self.register_vehicle()
                elif option == "4":
                    self.logout()
                else:
                    raise ValueError

            except SystemExit:
                CliComponent.thank_you()

            except ValueError:
                print("Ooops, try again.")
                get_option()

        get_option()


    def logout(self):
        """Logs a user out of the system and restarts the program."""
        CliComponent.thank_you()

        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.logged_in = False
        self.vehicles.clear()
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

        CliComponent.welcome_banner()
        self.login()


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

        @CliStyle.heading_1
        def user_stats_message():
            print(f"User Statistics for {self.fname} {self.lname}")

        self.calculate_user_stats()
        CliComponent.display_user_stats(self.total_journeys,
                                        self.total_co2_emitted,
                                        self.total_co2_offset)
        self.main_menu()

    def calculate_journey(self):
        journey = Journey(self.user_id)
        journey.input_locations()
        self.main_menu()

    # def register_vehicle(self):


def main():
    # instantiate cli
    cli = Walk2ZeroApp()
    cli
    # instantiate user
    user = User()
    # begin program
    user.login()


if __name__ == '__main__':
    main()
