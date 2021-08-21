from colorama import Fore

from db_utils import DbQuery as Db
import colorama


def calculate_user_stats(user_id):
    user_stats_dict = {
        "total_journeys": Db.get_total_user_journeys(user_id),
        "total_co2_emitted": Db.get_total_co2_emitted(user_id),
        "total_co2_offset": Db.get_total_co2_saved(user_id)
    }
    return user_stats_dict


def carbon_to_trees(carbon_offset):
    """
    Function to calculate offset and return the number of trees being planted the offset amounted to
    :param carbon_offset
    :return number of tree saved
    """
    carbon_to_co2_multiplier = 44 / 12  # atomic weights of CO2/C
    co2_offset = carbon_to_co2_multiplier * carbon_offset

    tree_co2_absorbed = 21772.416  # 1 tree can absorb 21,772.416 grams of CO2
    num_of_trees = co2_offset / tree_co2_absorbed

    trees = ''

    if num_of_trees < 1:
        trees = str(format(num_of_trees * 100, ".2f") + '% of a tree')
    elif num_of_trees == 1:
        trees = '1 tree'
    else:
        trees = '{} trees'.format(int(num_of_trees))

    if trees != 0:
        print(Fore.GREEN
              + "Your carbon offset amounted to "
              + trees +
              " being planted 🌳🌳🌳 Good job!")
        print('\033[39m')

    # return trees

