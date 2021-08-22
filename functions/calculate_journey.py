"""A collection of functions used to calculate a new journey.

This script contains various helper functions that are called by the main
script in order to calculate a new journey.
"""
from datetime import datetime
import numpy as np
import pandas as pd
import requests

import cli_components as cli
from db_utils import DbQuery as Db
import functions.menu_choices as menu
from config import API_KEY


# —————————————————————————————————————————————————————————————————————————————
# Calculate journey helper functions
# —————————————————————————————————————————————————————————————————————————————

def get_new_journey_id(user_id):
    """Return the journey id of the users next journey.

    Args:
        user_id (int): The unique ID of the user.
    Returns:
        int: Journey ID for the users next journey.
    """
    j_id = Db.get_max_journey_id(user_id)
    if j_id is None:
        return 1
    else:
        return j_id + 1


def get_datetime():
    """Return the current datetime."""
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_journey_data():
    """Return journey data from Google Maps API.

    This function calls input_locations, which asks for the user to input their
    origin and destination. It then provides the inputted locations to
    get_distances, which calls the Google Maps API to retrieve the required
    data.
    """
    input_origin, input_destination = input_locations()
    precise_origin, precise_destination, distances = get_distance(input_origin,
                                                                  input_destination)
    return precise_origin, precise_destination, distances


def input_locations():
    """Asks for user input to provide origin and destination locations.

    Returns:
        tuple: (origin, destination) where origin and destination are strings
               of the origin and destination locations inputted by the user.
    """
    origin = input("Enter your origin location: ")
    menu.option_to_exit(origin)
    try:
        if len(origin) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        return input_locations()

    destination = input("Enter your destination location: ")
    menu.option_to_exit(destination)
    try:
        if len(destination) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        return input_locations()

    return origin, destination


def get_distance(origin, destination):
    """Retrieves data from Google Maps API.

    This function takes the inputted origin and destination, then uses the
    Google Maps API to calculate the possible distances for the route according
    to the different modes of transport available. It calls the check_address
    function for the user to confirm that the addresses outputted by the API
    are the users intented addresses.

    Args:
        origin (str): origin location
        destination (str): destination location
    Returns:
        tuple: (precise_origin, precise_destination, distances) where
               precise_origin (str) is origin location outputted by the API and
               confirmed by the user, precise_destination (str) is the
               destination location outputted by the API and confirmed by the
               user and distances (dict) contains the journey distances by mode
               of transport.
    """
    api_key = API_KEY
    modes = ["driving", "walking", "bicycling", "transit"]
    distances = dict()

    try:
        for mode in modes:
            uri = f'https://maps.googleapis.com/maps/api/distancematrix/json?' \
                  f'origins={origin}&' \
                  f'destinations={destination}&' \
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

        precise_origin = origin_address[0]
        precise_destination = destination_address[0]
    except:
        print("Something has gone wrong!\n "
              "Try a new/clearer origin and destination.")
        return get_journey_data()

    if not check_address(precise_origin, precise_destination, distances):
        return get_journey_data()
    else:
        return precise_origin, precise_destination, distances


def check_address(origin, destination, distances):
    """Asks the user to confirm if the output address of the API are correct.

    This function takes user input ("1" or "2") to confirm whether the precise
    addresses found by the Google Maps API are the ones that they were
    expecting from the addresses they inputted.

    Args:
        origin (str): Precise origin outputted by the Google Maps API.
        destination(str): Precise destination outputted by the Google Maps API.
        distances(dict): Journey distances by transport mode.

    Returns:
        bool: True if users are happy with the addresses, false if the
              addresses were not what they were expecting and want to input
              them again.
    """
    cli.display_journey_address_check_options(origin, destination)
    option = input("Enter option number: ")
    menu.option_to_exit(option)
    try:
        if option == "1":
            print("Addresses accepted.")
            return True
        elif option == "2":
            print("Re-enter your origin and/or destination.")
            return False
        else:
            raise ValueError
    except ValueError:
        print("Ooops, try again.")
        return check_address(origin, destination, distances)


# —————————————————————————————————————————————————————————————————————————————
# Calculate journey emissions helper functions
# —————————————————————————————————————————————————————————————————————————————

def get_selection(distances, user_id):
    options_df = proposed_options(distances, user_id)
    user_choice = user_mode_selection(options_df)
    choice_dict = user_choice.to_dict(orient='records')[0]
    vehicle_id = choice_dict['Vehicle ID']
    carbon_emitted = choice_dict['Total Emissions']
    distance = choice_dict['Distance']

    options_emissions = options_df["Total Emissions"]
    max_emissions = options_emissions.max()
    carbon_saved = max_emissions - choice_dict['Total Emissions']

    return vehicle_id, carbon_emitted, carbon_saved, distance


def api_propose_modes(distances):
    """Returns distances for viable modes of transport based on distance.

    This function removes the "walking" and "bicycling" modes from the
    distances dictionary if the distance of the journey is greater than 5 km
    and 100 km respectively.

    Args:
        distances (dict): Distances for the calculated journey by mode of
                          transport as outputted by the Google Maps API.
    Returns:
        dict: Distances for the caluclated journey with keys removed for the
              unviable modes of transport.
    """
    distances = str_to_float(distances)
    if distances['walking'] > 5:
        del distances['walking']
    if distances['bicycling'] > 100:
        del distances['bicycling']
    return distances


def api_db_map():
    """Maps the API transport modes to those stored in the DB.

    This function maps the modes of transport outputted by the Google Maps API
    (walking, bicycling, driving and transit) to the transport methods stored
    in the vehicles table of the Walk2Zero DB.

    Returns:
        A pandas dataframe.
    """
    all_vehicles = Db.fetch_all_vehicles()

    # Convert list of tuples to df.
    df = pd.DataFrame(all_vehicles,
                      columns=['Vehicle ID',
                               'Vehicle Name',
                               'Carbon Emitted'])

    # Create list of conditions to match all_vehicles to API choices.
    conditions = [
        (df['Vehicle Name'] == 'foot'),

        (df['Vehicle Name'] == 'bicycle'),

        (df['Vehicle Name'] == 'motorbike') |
        (df['Vehicle Name'] == 'b_car') |
        (df['Vehicle Name'] == 'ph_car') |
        (df['Vehicle Name'] == 'petrol_car') |
        (df['Vehicle Name'] == 'diesel_car') |
        (df['Vehicle Name'] == 'taxi'),

        (df['Vehicle Name'] == 'transit')
    ]
    values = ['walking', 'bicycling', 'driving', 'transit']
    # create a new column and use np.select to assign values
    df['API choices'] = np.select(conditions, values)
    return df


def potential_options(user_id):
    """
    This function matches the user vehicles table to the API_DB map to list out
    potential modes of transport for the user. At this point, the function does
    not take into consideration the distance aspect.
    """
    user_vehicles = Db.fetch_user_vehicles(user_id)
    # Convert list of tuples to df.
    df_uv = pd.DataFrame(user_vehicles, columns=['User ID', 'Vehicle ID'])
    api_db_df = api_db_map()
    useroptions_df = pd.merge(api_db_df, df_uv, on='Vehicle ID', how='right')
    return useroptions_df


def proposed_options(distances, user_id):
    """
    Function that matches potential modes of transport to
    viable modes of transport depending on the API return to propose modes of
    transport.
    """
    api_return = api_propose_modes(distances)

    # Converting dict to df.
    api_options = pd.DataFrame(list(api_return.items()),
                               columns=['API choices', 'Distance'])
    useroptions_df = potential_options(user_id)
    Proposed_Options = pd.merge(useroptions_df,
                                api_options,
                                on='API choices',
                                how='right')

    # Calculate emissions based on the distance.
    Proposed_Options['Total Emissions'] = Proposed_Options['Carbon Emitted'] * \
                                          Proposed_Options['Distance']
    Proposed_Options = Proposed_Options.dropna()

    # Returning df of proposed options to push distance in to SQL DB.
    return Proposed_Options[['Vehicle ID',
                             'Vehicle Name',
                             'Distance',
                             'Total Emissions']]


def df_dict(df, col_list):
    """Convert Pandas df to dictionary.

    Args:
        df: Pandas dataframe.
        col_list: ['API choices','Total Emissions'] function call example
    Returns:
        dict: df_dict(proposed_mode,col_list)
    """
    dict1 = dict(df[col_list].values)
    return dict1


def str_to_float(distances):
    """Convert string distances to floats, removing "km".

    This function changes the string distances in in the dictionary distances
    from the Google Maps API and changes them into floats without "km".

    Args:
        distances (dict): Distances for the calculated journey by mode of
                          transport as outputted by the Google Maps API in
                          strings with "km" at the end.
    Returns:
        dict: Distances for the calculated journey as floats.
    """
    for key, value in distances.items():
        value = value.replace(',', '')
        distances[key] = float(value[:-3])
    return distances


def user_mode_selection(proposed_options):
    """Asks user to select transportation method for their journey.

    Returns:
        int: The vehicle ID of the transportation method they wish to take for
             their journey.
    """
    print("\nPlease select a Vehicle ID of your desired transport mode from the "
          "following options:\n")
    print(proposed_options[['Vehicle ID',
                            'Vehicle Name',
                            'Distance',
                            'Total Emissions']])
    choice = int(input("\nYour Vehicle ID selection: "))
    menu.option_to_exit(choice)
    chosen_mode = proposed_options.loc[proposed_options['Vehicle ID'] == choice]
    if chosen_mode.empty:
        print("Please enter a valid option from the Vehicle ID.")
        return user_mode_selection(proposed_options)
    else:
        return chosen_mode
