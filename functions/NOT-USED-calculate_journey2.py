"""A collection of functions used to calculate a new journey."""

from datetime import datetime
import requests

from db_utils import DbQuery as Db
import cli_components
import utils


# —————————————————————————————————————————————————————————————————————————————
# Main function to calculate a new journey
# —————————————————————————————————————————————————————————————————————————————

def calculate_new_journey(user_id):

    # Calculate new journey id (j_id in journeys table of DB).
    journey_id = get_new_journey_id(user_id)

    # Get datetime of journey.
    j_datetime = get_datetime()

    # Get desired origin and destination input from user.
    input_origin = get_journey_origin()
    input_destination = get_journey_destination()

    # Calculate precise addresses and distances with Google Maps API.
    precise_origin, precise_destination, distances = \
        get_journey_distances(user_id, input_origin, input_destination)
    # Example output:
    # ('Hull HU5 2DW, UK',
    #  'Bangor LL57 2BH, UK',
    #  {'driving': '313 km',
    #   'walking': '299 km',
    #   'bicycling': '334 km',
    #   'transit': '318 km'})

    # Check journey details are correct or start a new journey.
    if not check_address(precise_origin, precise_destination):
        calculate_new_journey(user_id)

    # Get vehicle selection for the new journey.
    vehicle_id, carbon_emitted, carbon_saved, distance = \
        journey_functions.get_selection(distances, user_id)

    output = {
        "journey_id": journey_id,
        "j_datetime": j_datetime,
        "origin": precise_origin,
        "destination": precise_destination,
        "distances": distances
    }

    return output




    # origin, destination = google_maps_api.input_locations()
    # origin, destination, distances = google_maps_api.get_distance(origin, destination)

    # set journey datetime
    # journey.set_journey_datetime()

    # set journey id
    # journey.get_journey_id(journey.user_id)  - check output

    # get journey locations
    # origin, destination, distances = journey_functions.output_locations()




# —————————————————————————————————————————————————————————————————————————————
# store to self and db
# —————————————————————————————————————————————————————————————————————————————
    # store journey locations to self
    journey.update_journey_locations(origin, destination)

    # store emissions to self
    journey.update_journey_emissions(vehicle_id, carbon_emitted, carbon_saved, distance)

    # save journey to db
    Db.write_journey(journey.user_id, journey.journey_id, journey.j_datetime, journey.origin, journey.destination,
                     journey.distance, journey.vehicle_id)

    # save emissions to db
    Db.write_journey_emissions(journey.user_id, journey.journey_id, journey.carbon_emitted, journey.carbon_saved)

    # print out of carbon offset data
    trees_calculator.carbon_to_trees(journey.carbon_saved)


# —————————————————————————————————————————————————————————————————————————————
# calculate_new_journey() helper functions
# —————————————————————————————————————————————————————————————————————————————

def get_datetime():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def get_new_journey_id(user_id):
    j_id = Db.get_max_journey_id(user_id)
    if j_id == 0:
        return 1
    else:
        return j_id + 1


def get_journey_origin():
    origin = input("Enter your origin location: ")
    utils.option_to_exit(origin)
    try:
        # Think of more/better end cases for these!
        if len(origin) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        get_journey_origin()
    else:
        return origin


def get_journey_destination():
    destination = input("Enter your origin location: ")
    utils.option_to_exit(destination)
    try:
        # Think of more/better end cases for these!
        if len(destination) < 2:
            raise ValueError
    except ValueError:
        print("That doesn't look right.\n"
              "Please try again.\n")
        get_journey_destination()
    else:
        return destination


def get_journey_distances(user_id, origin, destination):
    api_key = "AIzaSyATutmnPcuGNLy1JwV2FMksls1Q561WP9o"
    modes = ["driving", "walking", "bicycling", "transit"]
    distances = dict()
    # NOTE: move parts of try to else statement and raise exception for api error
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

        origin = origin_address[0]
        destination = destination_address[0]
    except:
        print("Something has gone wrong!\n"
              "Try a new/clearer origin and destination.")
        calculate_new_journey(user_id)

    return origin, destination, distances


def check_address(origin, destination):
    cli_components.display_journey_address_check_options(origin, destination)
    option = input("Enter option number: ")
    try:
        if option in ['q', 'Q']:
            cli_components.thank_you()
            exit()
        elif option == "1":
            print("Addresses accepted.")
            return True
        elif option == "2":
            print("Re-enter your origin and/or destination")
            return False
        else:
            raise ValueError
    except ValueError:
        print("Ooops, try again.")
        check_address(origin, destination)


# —————————————————————————————————————————————————————————————————————————————
# calculate_emissions() helper functions
# —————————————————————————————————————————————————————————————————————————————

def get_selection(distances, user_id):
    options_df = Propose_A_Mode.proposed_options(distances, user_id)
    user_choice = GeneralHelperFunc.user_mode_selection(options_df)
    choice_dict = user_choice.to_dict(orient='records')[0]
    vehicle_id = choice_dict['Vehicle ID']
    carbon_emitted = choice_dict['Total Emissions']
    distance = choice_dict['Distance']

    options_emissions = options_df["Total Emissions"]
    max_emissions = options_emissions.max()
    carbon_saved = max_emissions - choice_dict['Total Emissions']

    return vehicle_id, carbon_emitted, carbon_saved, distance


def api_propose_modes(distances):
    """
    This function removes the "walking" mode, from the distances dictionary,if the distance of the journey is greater
    than 5km as will no longer be a viable mode of transport.
    :param distances: distances as dictionary (as would be received from the function get_distance())
    :return: distances as dictionary only including the viable modes of transport
    """
    distances = GeneralHelperFunc.str_to_float(distances)
    if distances['walking'] > 5:
        del distances['walking']
    if distances['bicycling'] > 100:
        del distances['bicycling']
    return distances


def API_DB_map():
    """
    This function maps the API choices of walking, bicycling, driving and transit to our all vehicles table
    in the DB
    """
    all_vehicles = Db.fetch_all_vehicles()
    df = pd.DataFrame(all_vehicles, columns=['Vehicle ID', 'Vehicle Name', 'Carbon Emitted'])  # list of tuples to df conversion
    # creating a list of conditions to match all_vehicles to API choices
    conditions = [
        (df['Vehicle Name'] == 'foot'),
        (df['Vehicle Name'] == 'bicycle'),
        (df['Vehicle Name'] == 'motorbike') | (df['Vehicle Name'] == 'b_car') | (df['Vehicle Name'] == 'ph_car') | (
                df['Vehicle Name'] == 'petrol_car') | (df['Vehicle Name'] == 'diesel_car') | (df['Vehicle Name'] == 'taxi'),
        (df['Vehicle Name'] == 'transit')
    ]
    values = ['walking', 'bicycling', 'driving', 'transit']  # All API return choices
    # create a new column and use np.select to assign values
    df['API choices'] = np.select(conditions, values)
    return df

def potential_options(user_id):
    """
    This function matches the user vehicles table to the API_DB map to list out potential modes of transport for the user
    At this point, the function does not take into consideration the distance aspect.
    """
    user_vehicles = Db.fetch_user_vehicles(user_id)
    df_uv = pd.DataFrame(user_vehicles, columns=['User ID', 'Vehicle ID'])  # Converting list of tuples to df
    API_DB_df = Propose_A_Mode.API_DB_map()
    useroptions_df = pd.merge(API_DB_df, df_uv, on='Vehicle ID', how='right')
    return useroptions_df


def proposed_options(distances, user_id):  # would need to call the API Util func
    """
    Function that matches potential modes of transport to
    viable modes of transport depending on the API return to propose modes of transport
    """
    api_return = Propose_A_Mode.api_propose_modes(distances)
    api_options = pd.DataFrame(list(api_return.items()),
                               columns=['API choices', 'Distance'])  # converting dict to df
    useroptions_df = Propose_A_Mode.potential_options(user_id)
    Proposed_Options = pd.merge(useroptions_df, api_options, on='API choices', how='right')
    # Calculating emissions based on the distance
    Proposed_Options['Total Emissions'] = Proposed_Options['Carbon Emitted'] * Proposed_Options['Distance']
    Proposed_Options = Proposed_Options.dropna()
    # returning the df of proposed options as we need to push distance in to SQL DB.
    return Proposed_Options[['Vehicle ID', 'Vehicle Name', 'Distance', 'Total Emissions']]
