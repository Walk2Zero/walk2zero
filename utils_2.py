import pandas as pd
import numpy as np
import requests
from cli_components import CliComponent, CliStyle
from db_utils import DbQueryFunction as Db


# —————————————————————————————————————————————————————————————————————————————
# 'Proposed Modes of Transport' Helper Functions
# —————————————————————————————————————————————————————————————————————————————
class Propose_A_Mode:
    @staticmethod
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

    @staticmethod
    def API_DB_map():
        """
        This function maps the API choices of walking, bicycling, driving and transit to our all vehicles table
        in the DB
        """
        all_vehicles = Db.fetch_all_vehicles()
        df = pd.DataFrame(all_vehicles, columns=['v_id', 'v_name', 'e_value'])  # list of tuples to df conversion
        # creating a list of conditions to match all_vehicles to API choices
        conditions = [
            (df['v_name'] == 'foot'),
            (df['v_name'] == 'bicycle'),
            (df['v_name'] == 'motorbike') | (df['v_name'] == 'b_car') | (df['v_name'] == 'ph_car') | (
                    df['v_name'] == 'petrol_car') | (df['v_name'] == 'diesel_car') | (df['v_name'] == 'taxi'),
            (df['v_name'] == 'transit')
        ]
        values = ['walking', 'bicycling', 'driving', 'transit']  # All API return choices
        # create a new column and use np.select to assign values
        df['API choices'] = np.select(conditions, values)
        return df

    @staticmethod
    def potential_options(user_id):
        """
        This function matches the user vehicles table to the API_DB map to list out potential modes of transport for the user
        At this point, the function does not take into consideration the distance aspect.
        """
        user_vehicles = Db.fetch_user_vehicles(user_id)
        df_uv = pd.DataFrame(user_vehicles, columns=['user_id', 'v_id'])  # Converting list of tuples to df
        API_DB_df = Propose_A_Mode.API_DB_map()
        useroptions_df = pd.merge(API_DB_df, df_uv, on='v_id', how='right')
        return useroptions_df

    @staticmethod
    def proposed_options(distances, user_id):  # would need to call the API Util func
        """
        Function that matches potential modes of transport to
        viable modes of transport depending on the API return to propose modes of transport
        """
        api_return = Propose_A_Mode.api_propose_modes(distances)
        api_options = pd.DataFrame(list(api_return.items()),
                                   columns=['API choices', 'distance'])  # converting dict to df
        useroptions_df = Propose_A_Mode.potential_options(user_id)
        Proposed_Options = pd.merge(useroptions_df, api_options, on='API choices', how='right')
        # Calculating emissions based on the distance
        Proposed_Options['Total Emissions'] = Proposed_Options['e_value'] * Proposed_Options['distance']
        Proposed_Options = Proposed_Options.dropna()
        # returning the df of proposed options as we need to push distance in to SQL DB.
        return Proposed_Options[['v_id', 'v_name', 'distance', 'Total Emissions']]


# —————————————————————————————————————————————————————————————————————————————
# Vehicle Registration Functions
# —————————————————————————————————————————————————————————————————————————————
class VehicleReg:
    @staticmethod
    def vehicle_reg(user_id):
        # printing the menu
        all_vehicles = VehicleReg.uv_vehicle_map(user_id)
        print("Vehicle Registration Options:")
        for record in all_vehicles:
            print(record[0], record[1])
        # Converting the vehicle_ids into a list for comparison
        vehicle_ids = []
        for i in range(len(all_vehicles)):
            vehicle_ids.append(all_vehicles[i][0])

        def user_input():
            try:
                choices = [int(choices) for choices in
                           input("Enter the v_id of all the vehicles you wish to register(e.g. 1,2): ").split(",")]
                if all(x in vehicle_ids for x in choices):
                    print("Valid Selection!")
                else:
                    print("Invalid Selection. Please select again")
                    return user_input()
            except ValueError:
                print("Invalid selection. Please input again!")
                return user_input()
            else:
                for v_id in choices:
                    # print(user_id, v_id) for verification
                    Db.write_user_vehicles(user_id, v_id)
                print("Selection successful!")

        user_input()

    @staticmethod
    def uv_vehicle_map(user_id):
        # using list comprehension to filter out all the intersection of user-registered vehicles and vehicles in
        # the DB (c,d,e)->tuple o/p for vehicle db where c is v_id,d is mode, e is emissions value (a,
        # b)->tuple o/p for user-vehicle_db where a is user-id and b is vehicle-id
        all_vehicles = Db.fetch_all_vehicles()
        user_vehicles = Db.fetch_user_vehicles(user_id)
        registered_vehicles = [(c, d, e) for (c, d, e) in all_vehicles for (a, b) in user_vehicles if (c == b)]
        # filter repeated tuple
        not_registered_vehicles = [sub for sub in all_vehicles if sub not in registered_vehicles]
        return not_registered_vehicles


# Haven't worked on deleting the vehicles from the user registered vehicles table due to time constraint
# —————————————————————————————————————————————————————————————————————————————
# General Helper Functions
# —————————————————————————————————————————————————————————————————————————————
class GeneralHelperFunc:
    # Function to convert df to dictionary
    @staticmethod
    def df_dict(df, col_list):
        """
        Function to convert df to dictionary
        col_list = ['API choices','Total Emissions'] function call example
        dict2 = df_dict(proposed_mode,col_list)
        """
        dict1 = dict(df[col_list].values)
        return dict1

    @staticmethod
    def str_to_float(distances):
        """
        Function to change the string distances in in the dictionary distances from the API and changes them into floats
        without "km".
        :param distances: distances as dictionary (as would be received from the function get_distance())
        :return: distances as dictionary where the values are floats of the distance (km)
        """
        for key, value in distances.items():
            value = value.replace(',', '')
            distances[key] = float(value[:-3])
        return distances

    @staticmethod
    def user_mode_selection(proposed_options):
        print("\nPlease select a v_id of your desired transport mode from the following options:\n")
        print(proposed_options[['v_id', 'v_name', 'distance', 'Total Emissions']])
        choice = int(input("\nYour v_id selection: "))
        try:
            if choice in ['q', 'Q']:
                raise SystemExit
        except SystemExit:
            CliComponent.thank_you()
        chosen_mode = proposed_options.loc[proposed_options['v_id'] == choice]
        if chosen_mode.empty:
            print("Please enter a valid option from the v_id.")
            return GeneralHelperFunc.user_mode_selection(proposed_options)
        else:
            return chosen_mode


# —————————————————————————————————————————————————————————————————————————————
# API Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class google_maps_api:

    @staticmethod
    def input_locations():
        """
        This allows the user to input the locations of the origin and destination, assigns them to variables and returns
        these variables.

        :return: inputted origins and destination
        """
        origin = input("Enter your origin location: ")
        try:
            if origin in ['q', 'Q']:
                raise SystemExit
        except SystemExit:
            CliComponent.thank_you()
        destination = input("Enter your destination: ")
        try:
            if destination in ['q', 'Q']:
                raise SystemExit
        except SystemExit:
            CliComponent.thank_you()

        return origin, destination

    @staticmethod
    def get_distance(origin, destination):
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
            print("Something has gone wrong! \n Try a new/clearer origin and destination.")
            journey_functions.output_locations()

        origin, destination, distances = google_maps_api.check_address(origin, destination, distances)
        return origin, destination, distances

    @staticmethod
    def check_address(origin, destination, distances):
        print(f'\nYour origin address is: {origin}, \n'
              f'Your destination address is: {destination}. \n'
              f'Please select from the following options:\n'
              f'    (1) Address shown are correct. \n'
              f'    (2) Change Addresses \n')

        option = input("Enter option number: ")

        try:
            if option in ['q', 'Q']:
                raise SystemExit
            elif option == "1":
                print("Addresses accepted")
                return origin, destination, distances
            elif option == "2":
                print("Re-enter your origin and/or destination")
                journey_functions.output_locations()
            else:
                raise ValueError

        except SystemExit:
            CliComponent.thank_you()

        except ValueError:
            print("Ooops, try again.")
            google_maps_api.check_address()

        return origin, destination, distances


# —————————————————————————————————————————————————————————————————————————————
# Journey Helper Functions
# —————————————————————————————————————————————————————————————————————————————

class journey_functions:

    @staticmethod
    def output_locations():
        @CliStyle.heading_2
        def journey_heading():
            print("Enter Journey Details")

        origin, destination = google_maps_api.input_locations()
        origin, destination, distances = google_maps_api.get_distance(origin, destination)

        return origin, destination, distances

    @staticmethod
    def get_selection(distances, user_id):
        options_df = Propose_A_Mode.proposed_options(distances, user_id)
        user_choice = GeneralHelperFunc.user_mode_selection(options_df)
        choice_dict = user_choice.to_dict(orient='records')[0]
        vehicle_id = choice_dict['v_id']
        carbon_emitted = choice_dict['Total Emissions']
        distance = choice_dict['distance']

        options_emissions = options_df["Total Emissions"]
        max_emissions = options_emissions.max()
        carbon_saved = max_emissions - choice_dict['Total Emissions']

        return vehicle_id, carbon_emitted, carbon_saved, distance
