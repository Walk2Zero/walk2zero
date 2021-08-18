import re  # for checking email address against regex
from cli_components import CliStyle, CliComponent
from db_utils import DbQueryFunction as Db


class Walk2ZeroApp:

    def __init__(self):
        CliComponent.welcome_banner()


class User:

    def __init__(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.logged_in = False
        self.vehicles = {}
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

    # =========================================================================
    # Log In / Register
    # =========================================================================

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

    # =========================================================================
    # Main Menu
    # =========================================================================

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
                    print("calculate a journey function is called here")
                    # Journey.calculate_journey()
                elif option == "2":
                    self.display_stats()
                elif option == "3":
                    print("register vehicle function is called here")
                    self.register_vehicle()
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

    # -------------------------------------------------------------------------
    # Main Menu Option 1 – Calculate Journey
    # -------------------------------------------------------------------------

    # def calculate_journey(self):

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

        @CliStyle.heading_1
        def user_stats_message():
            print(f"User Statistics for {self.fname} {self.lname}")

        self.calculate_user_stats()
        CliComponent.display_user_stats(self.total_journeys,
                                        self.total_co2_emitted,
                                        self.total_co2_offset)
        self.main_menu()

    # -------------------------------------------------------------------------
    # Main Menu Option 3 – Register Vehicle
    # -------------------------------------------------------------------------

    def register_vehicle(self):

        @CliStyle.heading_1
        def user_stats_message():
            print(f"Register Vehicle")

        self.vehicles = Db.fetch_user_vehicles(self.user_id)

        # CliComponent.vehicle_registration_menu(user_id)
        # def get_option():
        #     option = input("Enter option number: ")
        # DB FUNCTION FOR WRITING TO DB GOES HERE.
        # NEEDS TO MATCH OPTION ENTERED WITH VEHICLE ID NUMBER.
        Db.write_user_vehicle(user_id, vehicle_id)

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
        self.logged_in = False
        self.vehicles.clear()
        self.total_journeys = 0
        self.total_co2_emitted = 0
        self.total_co2_offset = 0

        CliComponent.welcome_banner()
        self.login()


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
