"""Functions that facilitate user selection at the menus."""

import cli_components as cli


def option_to_exit(user_input):
    """Allows user to exit the program by typing 'q' or 'Q'."""
    if user_input in ['q', 'Q']:
        cli.thank_you()
        exit(0)


def main_menu_select_choice():
    """Allows user to enter which action to perform at the main menu."""
    selected_option = input("Enter option number: ")
    option_to_exit(selected_option)
    try:
        if selected_option not in ["1", "2", "3", "4"]:
            raise ValueError
    except ValueError:
        print("Ooops! Please enter an option number between 1 and 4.\n")
        return main_menu_select_choice()
    else:
        return int(selected_option)
