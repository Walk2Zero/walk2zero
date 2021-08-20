import pandas as pd
import numpy as np
from cli_components import CliComponent
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
        df = pd.DataFrame (all_vehicles, columns = ['v_id', 'v_name', 'e_value']) #list of tuples to df conversion
        #creating a list of conditions to match all_vehicles to API choices
        conditions = [
            (df['v_name'] == 'foot'),
            (df['v_name'] == 'bicycle'),
            (df['v_name'] == 'motorbike') | (df['v_name'] == 'b_car') | (df['v_name'] == 'ph_car') | (df['v_name'] == 'petrol_car') | (df['v_name'] == 'diesel_car') | (df['v_name'] == 'taxi'),
            (df['v_name'] == 'transit')
            ]
        values = ['walking', 'bicycling', 'driving', 'transit'] #All API return choices
            
        # create a new column and use np.select to assign values
        df['API choices'] = np.select(conditions, values)
        return df
        
    @staticmethod
    def potential_options():
        """
        This function matches the user vehicles table to the API_DB map to list out potential modes of transport for the user
        At this point, the function does not take into consideration the distance aspect.
        """
        user_vehicles = Db.fetch_user_vehicles()
        df_uv =  pd.DataFrame(user_vehicles, columns = ['user_id', 'v_id']) #Converting list of tuples to df
        API_DB_df = Propose_A_Mode.API_DB_map()
        useroptions_df = pd.merge(API_DB_df,df_uv,on='v_id',how='right')
        return useroptions_df
    
    @staticmethod
    def proposed_options(distances): #would need to call the API Util func
        """
        Function that matches potential modes of transport to 
        viable modes of transport depending on the API return to propose modes of transport
        """
        api_return = Propose_A_Mode.api_propose_modes(distances)
        api_options = pd.DataFrame(list(api_return.items()),columns = ['API choices','distance'])#converting dict to df
        useroptions_df = Propose_A_Mode.potential_options()
        Proposed_Options = pd.merge(useroptions_df,api_options,on='API choices',how='left')
        #Calculating emissions based on the distance
        Proposed_Options['Total Emissions'] = Proposed_Options['e_value'] * Proposed_Options['distance']
        #returning the df of proposed options as we need to push distance in to SQL DB.
        return Proposed_Options[['API choices','distance','Total Emissions']]

# —————————————————————————————————————————————————————————————————————————————
# General Helper Functions
# —————————————————————————————————————————————————————————————————————————————
class GeneralHelperFunc:

    #Function to convert df to dictionary
    @staticmethod
    def df_dict(df,col_list):
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