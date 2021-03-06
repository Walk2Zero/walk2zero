"""Command-Line Interface Components

This script contains methods that print the various components of the CLI and
methods that print decorative strings (e.g. lines) that make it easier to
understand where they are in the app.
"""
import pyfiglet


def welcome_banner():
    """Prints the Walk2Zero title banner."""
    banner = pyfiglet.figlet_format(text="Walk 2 Zero",
                                    font="standard",
                                    justify="center")
    slogan = "C L I M A T E   C O N S C I O U S   S T E P S"
    print(f"{banner}"
          f"{slogan:^80}"
          f"\n\n(To exit enter 'q')")


def header(text):
    return print(f"\n======================================================"
                 f"==========================\n"
                 f"{text}\n"
                 f"========================================================"
                 f"========================")


def display_main_menu():
    """Prints the main user menu."""
    print("Please select from the following options:\n\n"
          "    (1) plan journey\n"
          "    (2) view user stats\n"
          "    (3) register a vehicle\n"
          "    (4) log out\n")


def display_journey_address_check_options(origin, destination):
    """Displays journey addresses and options to confirm or change."""
    print(f"\nYour origin address is: {origin},\n"
          f"Your destination address is: {destination}.\n"
          f"Please select from the following options:\n"
          f"    (1) Addresses shown are correct.\n"
          f"    (2) Change Addresses.\n")


def display_user_stats(user_stats_dict):
    """Displays the user's statistics.

    This method prints the total carbon emitted and the total carbon
    offset by all journeys made by a user alongside some of their other
    key statistics.
    """
    print(f"Journeys made: "
          f"{user_stats_dict['total_journeys']}\n"
          f"CO2e emitted by all journeys: "
          f"{user_stats_dict['total_co2_emitted']}\n"
          f"CO2e offset by walking to zero: "
          f"{user_stats_dict['total_co2_offset']}\n")


# @staticmethod
# def vehicle_registration_menu(user_id):
#
#     all_vehicles = DbQueryFunction.fetch_all_vehicles()
#     user_vehicles = DbQueryFunction.fetch_user_vehicles(user_id)
#
#     # =====================================================================
#     # CURRENTLY WORKING ON THIS
#     # =====================================================================
#     # Need to remove options from all_vehicles where keys in user_vehicles
#     # match vehicle_name. Then store those left over in
#     # registrable_vehicles.
#
#     print(all_vehicles)  # [{'vehicle_id': 1, 'vehicle_name': 'foot', 'carb_emit_km': 0}, {'vehicle_id': 2, 'vehicle_name': 'bicycle', 'carb_emit_km': 0}, {'vehicle_id': 3, 'vehicle_name': 'motorbike', 'carb_emit_km': 145}, {'vehicle_id': 4, 'vehicle_name': 'b_car', 'carb_emit_km': 69}, {'vehicle_id': 5, 'vehicle_name': 'ph_car', 'carb_emit_km': 124}, {'vehicle_id': 6, 'vehicle_name': 'petrol_car', 'carb_emit_km': 223}, {'vehicle_id': 7, 'vehicle_name': 'diesel_car', 'carb_emit_km': 209}, {'vehicle_id': 8, 'vehicle_name': 'taxi', 'carb_emit_km': 259}, {'vehicle_id': 9, 'vehicle_name': 'transit', 'carb_emit_km': 127}]
#     print(user_vehicles)  # {'foot': 0, 'transit': 127}
#
#     registrable_vehicles = # needs to be {vehicle_id: vehicle_name}
#     print(registrable_vehicles)
#
#
#     print("You currently have the following modes of transport registered\n"
#           "to your account:")
#     for i in user_vehicles.keys():
#         print(f"    ??? {i}")
#
#     print("\nDo you want any of the following modes of transport to be\n"
#           "considered when planning a journey?")
#     option_number = 0
#     for i in registrable_vehicles.keys():
#         option_number += 1
#         print(f"    ({option_number}) {i}")



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
