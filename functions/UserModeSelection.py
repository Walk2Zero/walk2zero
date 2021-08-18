# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 22:53:16 2021

@author: laksh
"""

#Mock i/p
proposed_mode = {'walking': 0.0, 'bicycling': 117.6, 'driving': 324.3}

def user_mode_selection(proposed_mode):
    count = 0
    keys = list(proposed_mode)
    print("Please make your selection from the following options:")
    for key, value in proposed_mode.items():
        print('(',count,')',key, ' : ', value,'gm/km Co2e')
        count +=1

    try: 
        choice = int(input("Option:"))
        option = keys[choice]
        chosen_mode = {key: value for key, value in proposed_mode.items() if key == option}
        return chosen_mode
    
    except ValueError:
        print("Invalid selection.")
        return user_mode_selection(proposed_mode)
           
    except IndexError:
        print("Invalid selection.")
        return user_mode_selection(proposed_mode)
        
    else:
        option = keys[choice]
        chosen_mode = {key: value for key, value in proposed_mode.items() if key == option}
        return chosen_mode
             
#function test
output = user_mode_selection(proposed_mode)
print(output)

