import re  # for checking email address against regex
from cli_components import CliStyles
from db_utils import DbQueryFunctions as Db


class Cli:

    def __init__(self):
        CliStyles.welcome_banner()


class User:

    def __init__(self):
        self.user_id = None
        self.fname = None
        self.lname = None
        self.email = None
        self.logged_in = False

    def login(self):

        @CliStyles.heading_1
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
            CliStyles.thank_you()

        else:
            if Db.check_email(self.email):
                # print("Thank you. You are already registered.")
                self.verify_password()
                self.user_action()
            else:
                print("\nIt looks like you are a new user.")
                self.register()
                self.user_action()

    def verify_password(self):
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
            else:
                raise ValueError

        except SystemExit:
            CliStyles.thank_you()

        except ValueError:
            print("Incorrect password. Try again.")
            self.verify_password()

    def register(self):

        @CliStyles.heading_1
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
            CliStyles.thank_you()

        except ValueError:
            print("Ooops, that value isn't accepted.\n"
                  "Please try registering again.\n")
            self.register()

        else:
            Db.new_user(self.fname, self.lname, self.email, pword)
            self.user_id = Db.get_new_user_id(self.email)
            self.logged_in = True

    def user_action(self):

        @CliStyles.heading_1
        def user_menu_message():
            print(f"Welcome {self.fname}!")

        CliStyles.user_main_menu()

        def get_option():
            option = input("Enter option number: ")

            if option == "1":
                print("Calculate a journey")
            elif option == "2":
                print("Show user stats")
            elif option == "3":
                print("Add transport method")
            elif option == "4":
                print("Log user out")
            else:
                print("Ooops, try again.")
                get_option()

        get_option()


    # @staticmethod
    # def logout():
    #     CliStyles.thank_you()
    #     CliStyles.welcome_banner()
    #     user = User()
    #     user.login()


# class Journey:
#
#     def __init__(self):


def main():
    # instantiate cli
    cli = Cli()
    cli
    # instantiate user
    user = User()
    # begin program
    user.login()


if __name__ == '__main__':
    main()

