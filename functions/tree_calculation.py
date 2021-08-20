import colorama
from colorama import Fore
colorama.init()

def carbon_to_trees(carbon_offset):
    """
    Function to calculate offset and return the number of trees being planted the offset amounted to
    :param carbon_offset
    :return number of tree saved
    """
    carbon_to_co2_multiplier = 44/12 # atomic weights of CO2/C
    co2_offset = carbon_to_co2_multiplier * carbon_offset

    tree_co2_absorbed = 21772.416 # 1 tree can absorb 21,772.416 grams of CO2
    num_of_trees = co2_offset / tree_co2_absorbed

    trees = ''

    if num_of_trees < 1:
        trees = str(format(num_of_trees * 100, ".2f") + '% of a tree')
    elif num_of_trees == 1:
        trees = '1 tree'
    else:
        trees = '{} trees'.format(int(num_of_trees))

    print(Fore.GREEN
          + "Your carbon offset amounted to "
          + trees +
          " being planted 🌳🌳🌳 Good job!")

    return trees


carbon_to_trees(870)

carbon_to_trees(87000)





