"""A collection of functions used to calculate statistics.

This script contains helper functions that calculate the statistics outputted
by the Walk2Zero app.
"""


from colorama import Fore

from db_utils import DbQuery as Db


def calculate_user_stats(user_id):
    """Calculates the users total journeys, CO2 emitted and CO2 offset.

    Args:
        user_id (int): Unique ID number of the user.
    Returns:
        dict: The total number of journeys made, total amount of CO2 emitted by
              those journeys and the total amount of CO2 offset by the user.
    """
    user_stats_dict = {
        "total_journeys": Db.get_total_user_journeys(user_id),
        "total_co2_emitted": Db.get_total_co2_emitted(user_id),
        "total_co2_offset": Db.get_total_co2_saved(user_id)
    }
    return user_stats_dict


def carbon_to_trees(carbon_offset):
    """Calculates the carbon offset equivalent in number of trees planted.

    This function calculates the number of trees the user would have had to
    plant in order to offset the amount of carbon they have saved on their
    journey.

    Args:
        carbon_offset (int): Amount of carbon offset on a journey (in grams).
    Returns:
        A print statement detailing the number of trees they would have had to
        plant.
    """
    carbon_to_co2_multiplier = 44 / 12  # atomic weights of CO2/C
    co2_offset = carbon_to_co2_multiplier * carbon_offset

    tree_co2_absorbed = 21772.416  # 1 tree can absorb 21,772.416 grams of CO2
    num_of_trees = co2_offset / tree_co2_absorbed

    if num_of_trees == 1 or num_of_trees == 0:
        trees = '{} tree'.format(int(num_of_trees))
    elif num_of_trees > 1:
        trees = '{} trees'.format(int(num_of_trees))
    else:
        trees = str(format(num_of_trees * 100, ".2f") + '% of a tree')

    print(Fore.GREEN
          + "Your carbon offset amounted to the equivalent of"
          + trees +
          " being planted 🌳🌳🌳 Good job!")
    print('\033[39m')

    return trees
