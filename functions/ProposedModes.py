# -*- coding: utf-8 -*-
"""
Created on Mon Aug 16 16:55:12 2021

@author: laksh
"""
#Function to choose specific mode of transport
import pandas as pd
import numpy as np

"""Mock Inputs"""
#args to the functions
vehicle_DB = [(1, 'foot', 0), (2, 'bicycle', 21), (3, 'b_car', 69), (4, 'motorbike', 145), (5, 'ph_car', 124), (6, 'petrol_car', 223), (7, 'diesel_car', 209),(8, 'taxi', 259), (9, 'transit', 127)]

#(user id,vehicle id) as a tuple; assumption is that it only returns the vehicles for 1 user at a time i.e. all vehicles for one user id                               
user_vehicles_DB = [(1, 1), (1, 2),(1,3)] 

#API return from Proposed Options function - API Raw
Mock_API_return = {'driving': 4.7, 'walking': 7.0, 'bicycling': 5.6, 'transit': 5.2}

"""Functions"""

#Function that matches the vehicle DM to all options of travel medium possible proposed by the API
def API_DB_map(vehicle_DB): 
    df = pd.DataFrame (vehicle_DB, columns = ['v_id', 'v_name', 'e_value']) #list of tuples to df conversion
    
    #creating a list of conditions to match vehicle_DB to API choices
    conditions = [
        (df['v_name'] == 'foot'),
        (df['v_name'] == 'bicycle'),
        (df['v_name'] == 'motorbike') | (df['v_name'] == 'b_car') | (df['v_name'] == 'ph_car') | (df['v_name'] == 'petrol_car') | (df['v_name'] == 'diesel_car') | (df['v_name'] == 'taxi'),
        (df['v_name'] == 'transit')
        ]
    values = ['walking', 'bicycling', 'driving', 'transit'] #API Choices
    
    # create a new column and use np.select to assign values
    df['API choices'] = np.select(conditions, values)
    return df

#Function that matches the vehicle DB to user vehicles DB to list out potential modes of transport for the user
#At this point, the function does not take into consideration the distance aspect.
def potential_options(user_vehicles_DB,vehicle_DB):
    df_uv =  pd.DataFrame(user_vehicles_DB, columns = ['user_id', 'v_id']) #List of tuples conversion to df
    API_DB_df = API_DB_map(vehicle_DB)
    useroptions_df = pd.merge(API_DB_df,df_uv,on='v_id',how='right')
    return useroptions_df

#Function that matches potential modes of transport to viable modes of transport depending on the API return to propose modes of transport
def proposed_options(Mock_API_return,user_vehicles_DB,vehicle_DB):
    Mock_API_return = pd.DataFrame(list(Mock_API_return.items()),columns = ['API choices','distance'])
    useroptions_df = potential_options(user_vehicles_DB,vehicle_DB)
    Proposed_Options = pd.merge(useroptions_df,Mock_API_return,on='API choices',how='left')
    #Calculating emissions based on the distance
    Proposed_Options['Total Emissions'] = Proposed_Options['e_value'] * Proposed_Options['distance']
    #returning the df of proposed options as we need to push distance in to SQL DB.
    return Proposed_Options[['API choices','distance','Total Emissions']]

#Function to convert df to dictionary
def df_dict(df,col_list):
    dict1 = dict(df[col_list].values)
    return dict1

#Demo
proposed_mode = proposed_options(Mock_API_return,user_vehicles_DB,vehicle_DB)   
col_list = ['API choices','Total Emissions'] 
dict2 = df_dict(proposed_mode,col_list)
    
    

    
                                                                                                                         