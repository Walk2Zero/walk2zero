"""Command-Line Interface Components

This script contains methods that print the various components of the CLI and
methods that print decorative strings (e.g. lines) that make it easier to
understand where they are in the app.
"""


import pyfiglet


class CliComponent:
    """A class to contain command-line components, e.g. banners, menus etc."""

    @staticmethod
    def welcome_banner():
        """Prints the Walk2Zero title banner."""
        banner = pyfiglet.figlet_format(text="Walk 2 Zero",
                                        font="standard",
                                        justify="center")
        slogan = "C L I M A T E   C O N S C I O U S   S T E P S"
        print(f"{banner}"
              f"{slogan:^80}"
              f"\n\n(To exit enter 'q')")

    @staticmethod
    def user_main_menu():
        """Prints the main user menu."""
        print("Please select from the following options:\n\n"
              "    (1) plan journey\n"
              "    (2) view user stats\n"
              "    (3) register a vehicle\n"
              "    (4) log out\n")

    @staticmethod
    def thank_you():
        """Prints a thank you and goodbye message."""
        ty_message_l1 = "T H A N K   Y O U   F O R   T A K I N G"
        ty_message_l2 = "C L I M A T E   C O N S C I O U S   S T E P S"
        ty_message_l3 = "G O O D B Y E"
        ty_message_l4 = "- - - - - - - - - - - - - - - - - - - - - - -"
        print(f"\n{ty_message_l1:^80}"
              f"\n{ty_message_l2:^80}"
              f"\n\n{ty_message_l3:^80}"
              f"\n\n{ty_message_l4:^80}\n\n")


class CliStyle:
    """A class to contain decorators that visually improve the CLI.

    These decorators act as styles (think heading styles in Microsoft Word that
    visually improve the CLI and help to delineate movement between different
    sections of the program.
    """

    @staticmethod
    def heading_1(func):
        print("\n=============================================================="
              "==================")
        func()
        print("=============================================================="
              "==================")

    @staticmethod
    def heading_2(func):
        func()
        print("\n--------------------------------------------------------------"
              "------------------")
